from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, status, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from books.models import Author, Book, Comment, Genre
from books.serializers import AuthorSerializer, BookSerializer, CommentReadSerializer, CommentWriteSerializer, GenreSerializer

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView

from books.permissions import IsAuthorOrReadOnly
from books import serializers

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

# class BookDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         book = self.get_object(pk)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)


class GenreListAPIView(ListCreateAPIView):
    queryset=Genre.objects.all()
    serializer_class=GenreSerializer
    # permission_classes = (permissions.AllowAny,)
    
    # def get(self, request):
    #     genres=Genre.objects.all()
    #     genre_list=[genres.name for genre in genres]
    #     return Response(genre_list)

# class GenreViewSet(viewsets.ViewSet):
#     def list(self, request):
#         genre=Genre.objects.all()
#         serializer=GenreSerializer(genre, many=True)
#         return Response(serializer.data)


class AuthorListAPIView(ListCreateAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        book_id = self.kwargs.get("book_id")
        return res.filter(book__id=book_id)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer

        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

# Here, we are using the normal APIView class
class LikeBookAPIView(APIView):
    """
    Like, Dislike a post
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        book = get_object_or_404(Book, pk=pk)

        if user in book.likes.all():
            book.likes.remove(user)

        else:
            book.likes.add(user)

        return Response(status=status.HTTP_200_OK)
