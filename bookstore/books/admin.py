from django.contrib import admin
from books.models import Book
from books.models import Genre
from books.models import Author
from books.models import Comment
from books.models import BookRating
# from books.models import BookStatus


admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(BookRating)
# admin.site.register(BookStatus)


