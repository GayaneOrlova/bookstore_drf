from bookstore.settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from users.models import CustomUser



class Cart(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField("CartItem")
    # total_price = models.DecimalField(max_digits=8, decimal_places=2)
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)
   # quantity = models.PositiveIntegerField()    
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
    # carts = models.ForeignKey(Cart, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        total_price = self.book.price * self.amount
        return  total_price
    
    def delete(self):
        # when deleting a cart item, we need to restore the store_amount of the book
        book = Book.objects.get(pk=self.book.id)
        book.store_amount += self.amount
        book.save()
        super(CartItem, self).delete()
        
    def __str__(self):
        return f"Cart Item {self.id} (Book {self.book})"
    
# class CartItem(models.Model):
#     cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name='items')
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     amount = models.IntegerField(default=1)
    
#     @property
#     def total_price(self):
#         return self.book.price * self.amount
    
#     def delete(self):
#         # when deleting a cart item, we need to restore the store_amount of the book
#         book = Book.objects.get(pk=self.book.id)
#         book.store_amount += self.amount
#         book.save()
#         super(CartItem, self).delete()
        
#     def __str__(self):
#         return f"Cart {self.cart}'s Item {self.id} (Book {self.book})"

# class Cart(models.Model):
#     user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
#     cart_items = models.ManyToManyField(CartItem)
#     bought = models.BooleanField(default=0) # if the cart has been checkedout
    
#     @property
#     def total_price(self):
#         total = 0
#         for item in self.items.all():
#             total += item.total_price
#         return total
    
#     def __str__(self):
#         return f"User {self.user}'s Cart {self.id}"


