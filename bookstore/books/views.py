from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView
from books.models import Author, Book, Comment, Genre, BookRating
from books.serializers import AuthorSerializer, BookSerializer, BookRatingSerializer, CommentSerializer, CommentPostSerializer, GenreSerializer
from books.serializers import BookRatingCreateSerializer

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

class CommentView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Comment.objects.filter(book_id=book_id)

class CommentCreateView(CreateAPIView):
        serializer_class = CommentPostSerializer
        permission_classes = [permissions.IsAuthenticated]

        def perform_create(self, serializer):
            serializer.save(user=self.request.user, avatar=self.request.user.avatar)
    
class LikeBookAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        book = get_object_or_404(Book, pk=pk)

        if user in book.likes.all():
            book.likes.remove(user)

        else:
            book.likes.add(user)

        return Response(status=status.HTTP_200_OK)

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
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRatingDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        user = request.user

        try:
            rating = BookRating.objects.get(book=book, user=user)
            serializer = BookRatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BookRating.DoesNotExist:
            return Response("Рейтинг не найден")


class LikedBooksListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(likes=user)




