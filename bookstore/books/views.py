from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from books.models import Author, Book, Comment, Genre, BookFavorite, BookRating
from books.serializers import AuthorSerializer, BookFavoriteSerializer, BookSerializer, BookRatingSerializer, CommentSerializer,CommentCreateSerializer, GenreSerializer, FavoriteListSerializer
from django.db.models import Q

from firebase_admin import messaging
from firebase_admin.messaging import (Message, Notification)

from more_itertools import batched

from bookstore.settings import AUTH_USER_MODEL
from users.models import DeviceTypes
from users.models import UserDevice

MAX_MESSAGES_PER_BATCH = 500

class GenreFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genres = request.GET.getlist('genre')
        if genres:
            q_objects = Q()
            for genre in genres:
                q_objects |= Q(genre__name=genre)
            queryset = queryset.filter(q_objects).distinct()
        return queryset

class PriceRangeFilterBackend(BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            if min_price and max_price:
                queryset = queryset.filter(price__range=(min_price, max_price))
            elif min_price:
                queryset = queryset.filter(price__gte=min_price)
            elif max_price:
                queryset = queryset.filter(price__lte=max_price)
            return queryset

class BookListAPIView(ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    pagination_class = PageNumberPagination
    filter_backends = [GenreFilter, OrderingFilter, PriceRangeFilterBackend, SearchFilter]
    ordering_fields = ['price', 'title', 'author', 'overall_rating', 'published_at']
    search_fields = ['title', 'author__name']


class BookViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        
        book=Book.objects.get(pk=pk)
        serializer=BookSerializer(book, context={"request": request})
        return Response(serializer.data)
        
class BookRecommendationView(APIView):
    def get_queryset(self):
        return Book.objects.filter(recommendation=True)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class GenreListAPIView(ListCreateAPIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

class AuthorListAPIView(ListCreateAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer

class CommentListView(APIView):        
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            comments = Comment.objects.filter(book=book)
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            
            send_push(serializer.instance)
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def send_push(comment):
    tokens = UserDevice.objects.filter(type=DeviceTypes.ANDROID).exclude(user = comment.user)
    messages = []
    for token in tokens:
        messages.append(Message(token=token.firebase_token, notification=Notification(title=f"User {comment.user.username} left a comment on the book {comment.book.title}"
, body=comment.body), data={"comment_type": "comment_notification", "bookId": str(comment.book.id)}))
    responses = []
    
    for batch_messages in batched(messages, MAX_MESSAGES_PER_BATCH):
        responses.extend(messaging.send_all(list(batch_messages)).responses)
        
    response = messaging.BatchResponse(responses)


class BookRatingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        user = request.user

        try:
            rating = BookRating.objects.get(book=book, user=user)
            return Response("Рейтинг уже стоит", status=status.HTTP_400_BAD_REQUEST)
        except BookRating.DoesNotExist:
            serializer = BookRatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(book=book, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class BookRatingDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        user = request.user
        try:
            rating = BookRating.objects.get(book=book, user=user)
            serializer = BookRatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BookRating.DoesNotExist:
            return Response({"rating": None})

class FavoriteListView(APIView):
    def get(self, request):
        user_id = request.user.id
        
        favorite_items = BookFavorite.objects.filter(user_id=user_id)
        serializer = FavoriteListSerializer(favorite_items, many=True, context={'request': request})
        return Response(serializer.data)

class FavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        book_id = request.data.get('id')
        user_id = request.user.id
        
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response("Book does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book_like = BookFavorite.objects.get(user_id=user_id, book_id=book_id)
            book_like.delete()
            return Response("Item removed from favorites", status=status.HTTP_200_OK)
        except BookFavorite.DoesNotExist:
            book_like = BookFavorite.objects.create(user_id=user_id, book_id=book_id)
            serializer = BookFavoriteSerializer(book_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchAPIView(APIView):
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author__name']

    def get(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)