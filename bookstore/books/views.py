from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from books.models import Author, Book, Comment, Genre, BookRating
from books.serializers import AuthorSerializer, BookFavoriteSerializer, BookSerializer, BookRatingSerializer, CommentSerializer,CommentCreateSerializer, GenreSerializer
from books.models import BookFavorite
from . import serializers

class BookListAPIView(ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    
class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        books=Book.objects.all()
        serializer=BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        book=Book.objects.get(pk=pk)
        serializer=BookSerializer(book, context={"request": request})
        return Response(serializer.data)

class GenreListAPIView(ListCreateAPIView):
    queryset=Genre.objects.all()
    serializer_class=GenreSerializer

class AuthorListAPIView(ListCreateAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer

class CommentListView(APIView):        
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            comments = Comment.objects.filter(book=book)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class BookRatingCreateView(APIView):
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
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = BookFavoriteSerializer(favorite_items, many=True, context={'request': request})
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


