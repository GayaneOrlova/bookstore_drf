from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from books.models import Author, Book, Comment, Genre, BookRating
from books.serializers import AuthorSerializer, BookSerializer, BookRatingCreateUpdateSerializer, BookRatingSerializer, CommentSerializer, GenreSerializer

class BookListAPIView(ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer

class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        books=Book.objects.all()
        serializer=BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        book=Book.objects.get(pk=pk) #сделать возврат пустого ответа -нет такой книги
        serializer=BookSerializer(book)
        return Response(serializer.data)

class GenreListAPIView(ListCreateAPIView):
    queryset=Genre.objects.all()
    serializer_class=GenreSerializer


class AuthorListAPIView(ListCreateAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Comment.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        serializer.save(book_id=book_id)
    

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


