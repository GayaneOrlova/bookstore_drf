from rest_framework import serializers
from books.serializers import BookSerializer
from books.models import Book
from cart.models import  CartItem

class CartItemSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.title")
    book_author = serializers.CharField(source="book.author")
    id = serializers.IntegerField()
    amount = serializers.IntegerField(default=1)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    book_image = serializers.SerializerMethodField()

    def get_book_image(self, obj):
        request = self.context.get('request')
        image_url = obj.book.image.url
        return request.build_absolute_uri(image_url)
    class Meta:
        model = CartItem
        fields = ['amount', 'price', 'book_name', 'id', 'book_image', "book_author"]
