from bookstore.settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from users.models import CustomUser



class Cart(models.Model):
    items = models.ManyToManyField("CartItem")  
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total
    
    def __str__(self):
        return f"User {self.user}'s Cart {self.id}"
    
    
class CartItem(models.Model):
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        return self.book.price * self.amount
    
    def delete(self):
        book = Book.objects.get(pk=self.book.id)
        book.store_amount += self.amount
        book.save()
        super(CartItem, self).delete()
        
    def __str__(self):
        return f"Cart {self.carts}'s Item {self.id} (Book {self.book})"



