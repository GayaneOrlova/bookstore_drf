from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from books.serializers import BookSerializer

from books.models import Book
from books.models import Genre
from rest_framework import viewsets
from books.serializers import GenreSerializer
from books.models import Author
from books.serializers import AuthorSerializer


class BookListAPIView(ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer

    # def get(self, request):
    #     books=Book.objects.all()
    #     books_list=[book.title for book in books]
    #     return Response(books_list)

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
    
    # def get(self, request):
    #     genres=Genre.objects.all()
    #     genre_list=[genres.name for genre in genres]
    #     return Response(genre_list)

class AuthorListAPIView(ListCreateAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer