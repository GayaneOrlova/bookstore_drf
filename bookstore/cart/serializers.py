from rest_framework import serializers
from books.serializers import BookSerializer
from cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False)
    amount = serializers.IntegerField(default=1)
    total_price = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.total_price