from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView
from books.models import Author, Book, Comment, Genre, BookRating
from books.serializers import AuthorSerializer, BookLikeSerializer, BookSerializer, BookRatingSerializer, CommentSerializer, CommentPostSerializer, GenreSerializer
from books.models import BookLike
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
     
class CommentCreateView(CreateAPIView):
    serializer_class = CommentPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError('Invalid book_id')
        serializer.save(user=self.request.user, book=book)
    
class CommentListView(APIView):        
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            comments = Comment.objects.filter(book=book)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


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


# class LikedBooksListView(ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = BookSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Book.objects.filter(likes=user)







# class AddToFavoriteView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request):
#         book_id = request.data.get('id')
#         user_id = request.user.id
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response("Invalid book ID", status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             book_like = BookLike.objects.get(user_id=user_id, book_id=book_id)
#             return Response("Item already added to favorites", status=status.HTTP_400_BAD_REQUEST)
#         except BookLike.DoesNotExist:
#             book_like = BookLike.objects.create(user_id=user_id, book_id=book_id)
#             serializer = BookLikeSerializer(book_like)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
      


# class RemoveFromFavoriteView(APIView):
#     def post(self, request):
#         book_id = request.data.get('id')
#         user_id = request.user.id
        
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response("Invalid book ID", status=status.HTTP_400_BAD_REQUEST)
        
        
#         try:
#             book_like = BookLike.objects.get(user_id=user_id, book_id=book_id)
#             book_like.delete()
#             return Response("Item removed from favorites")
#         except BookLike.DoesNotExist:
#             return Response("Item not found in favorites", status=status.HTTP_404_NOT_FOUND)

class FavoriteListView(APIView):
    def get(self, request):
        user_id = request.user.id
        
        favorite_items = BookLike.objects.filter(user_id=user_id)
        serializer = BookLikeSerializer(favorite_items, many=True, context={'request': request})
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
            book_like = BookLike.objects.get(user_id=user_id, book_id=book_id)
            book_like.delete()
            return Response("Item removed from favorites", status=status.HTTP_200_OK)
        except BookLike.DoesNotExist:
            book_like = BookLike.objects.create(user_id=user_id, book_id=book_id)
            serializer = BookLikeSerializer(book_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
