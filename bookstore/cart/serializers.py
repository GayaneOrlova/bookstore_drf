from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from cart.models import CartItem
from cart.models import Cart

# class CartSerializer(serializers.ModelSerializer):
#     books = BookSerializer(many=True)

#     class Meta:
#         model = Cart
#         # fields = '__all__'
#         fields = ['user', 'books', 'total_price']

#     def update(self, instance, validated_data):
#         books_data = validated_data.pop('books')
#         instance.user = validated_data.get('user', instance.user)
#         instance.total_price = validated_data.get('total_price', instance.total_price)

#         instance.books.clear()
#         for book_data in books_data:
#             book = Book.objects.get(pk=book_data['id'])
#             instance.books.add(book)

#         instance.save()
#         return instance


# class CartItemSerializer(serializers.ModelSerializer):
#     book = BookSerializer()
#     class Meta:
#         model = CartItem
#         fields = ['book', 'quantity']

# class CartSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     cart_item = CartItemSerializer(many=True)
    
#     class Meta:
#         model = Cart
#         fields = ['user', 'cart_item', 'total_price']


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False)
    amount = serializers.IntegerField(default=1)
    total_price = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['total_price', 'book', 'amount']
        # depth = 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Cart
        fields = '__all__'
    #     depth = 0

    # def get_total_price(self, obj):
    #     return obj.total_price