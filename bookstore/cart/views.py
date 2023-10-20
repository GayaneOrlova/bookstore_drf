from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from books.models import Book
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer

class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        try: 
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"items": [], "price": None})
 
        items = CartItem.objects.filter(cart=cart)
        total_price = sum([item.price for item in items])
        serializer = CartItemSerializer(items, many=True, context={'request': request})
        return Response({"items": serializer.data, "total_price": total_price})

class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_item_id = request.data.get('id')
        amount = request.data.get('amount')
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response("CartItem does not exist", status=status.HTTP_404_NOT_FOUND)

        if amount > 0:
            # if amount <= cart_item.book.store_amount:
            cart_item.amount = amount
            cart_item.save()
            updated_cart_item = CartItem.objects.get(id=cart_item_id)
            serializer = CartItemSerializer(updated_cart_item, context={'request': request})
            return Response(serializer.data)
            # else:
            #     return Response("Cannot add more books than available", status=status.HTTP_400_BAD_REQUEST)

        if amount == 0:
            cart_item = CartItem.objects.get(id = cart_item_id)
            cart_item.delete()
            return Response('CartItem deleted')
            
        raise RuntimeError("not correct")


class AddToCartView(APIView):
    def post(self, request):
        book_id = request.data.get('id')
        user_id = request.user.id
        
        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user_id=user_id)
        
        book = get_object_or_404(Book, id=book_id) 
        
        try:
            cart_item = CartItem.objects.get(cart=cart, book=book)
            cart_item.amount += 1
            cart_item.save()
            
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, book=book)
        serializer = CartItemSerializer(cart_item, context={'request': request})
        return Response(serializer.data)            
