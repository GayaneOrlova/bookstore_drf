from django.contrib import admin
from books.models import Book
from books.models import Genre
from books.models import Author


admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Author)
