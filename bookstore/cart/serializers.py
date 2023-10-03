from rest_framework import serializers
from books.serializers import BookSerializer
from books.models import Book
from cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.title")
    book_image = serializers.CharField(source="book.image")
    
    

    id = serializers.IntegerField()
    amount = serializers.IntegerField(default=1)
    total_price = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['amount', 'total_price', 'book_name', 'id', 'book_image']
