from django.db import models
from django.contrib.auth.models import User
from books.models import Book
# from user.models import BookstoreUser


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Cart(models.Model):
    # user = models.ForeignKey(BookstoreUser, on_delete=models.CASCADE)
    cart_item = models.ManyToManyField(CartItem)

