from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView
from books.models import Author, Book, Comment, Genre, BookRating
from books.serializers import AuthorSerializer, BookSerializer, BookRatingCreateUpdateSerializer, BookRatingSerializer, CommentSerializer, CommentPostSerializer, GenreSerializer


class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        books=Book.objects.all()
        serializer=BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        book=Book.objects.get(pk=pk)
        serializer=BookSerializer(book)
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

class BookRatingListCreateView(ListCreateAPIView):
    queryset = BookRating.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookRatingCreateUpdateSerializer
        return BookRatingSerializer

class BookRatingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = BookRating.objects.all()
    serializer_class = BookRatingSerializer

class BookRatingUpdateView(UpdateAPIView):
    queryset = BookRating.objects.all()
    serializer_class = BookRatingCreateUpdateSerializer


