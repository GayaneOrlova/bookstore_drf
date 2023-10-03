from bookstore.settings import AUTH_USER_MODEL
from django.db import models
from books.models import Book
from users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"User {self.user}'s Cart {self.id}"
    
class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    @property
    def total_price(self):
        return self.book.price * self.amount
        
    # @property
    # def book_image(self):
    #     books = models.ForeignKey(Book, on_delete=models.CASCADE)
    #     try:
    #         book_images = Book.objects.get(image=books)
    #     except ObjectDoesNotExist:
    #         return None
    #     return book_images.image
    
    
    def __str__(self):
        return f"Item {self.id} (Book {self.book})"



