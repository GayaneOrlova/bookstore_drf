from django.shortcuts import get_object_or_404, render
from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from books.models import Book
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer

class CartAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        book_id = request.data.get('id')
        book = get_object_or_404(Book, id= book_id)
        cart = Cart.objects.get(user=request.user)
    
        item = cart.items.filter(book=book).first()
    
        if item:
            item.amount += 1
            item.save()
        else:
            item = CartItem.objects.create(book=book)
            cart.items.add(item)
    
        book.store_amount -= 1
        book.save()
    
        return Response("Book added to cart successfully")

class DeleteFromCartView(APIView):
    def post(self, request):
        book_id = request.data.get('id')
        item = get_object_or_404(CartItem, id=book_id)
        cart = Cart.objects.get(user=request.user)
        
        # Update the store amount of the book
        item.book.store_amount += item.amount
        item.book.save()
        
        # Remove the item from the cart
        cart.items.remove(item)
        
        return Response("Item removed from cart successfully")
