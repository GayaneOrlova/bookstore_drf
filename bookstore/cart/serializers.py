from rest_framework import serializers

from books.models import Book
from cart.models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'