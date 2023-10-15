from bookstore.settings import AUTH_USER_MODEL
from django.db import models
from books.models import Book
from users.models import CustomUser

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"User {self.user}'s Cart {self.id}"
    
class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    @property
    def price(self):
        return self.book.price * self.amount
    
    def __str__(self):
        return f"Item {self.id} (Book {self.book})"



