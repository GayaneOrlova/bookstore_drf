from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from cart.serializers import CartSerializer
from rest_framework import generics
from cart.models import Cart
from rest_framework.response import Response

# class CartAPIView(ListCreateAPIView):
#     queryset=Cart.objects.all()
#     serializer_class=CartSerializer(many=True)

#     def post(self, request):
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CartAPIView(generics.RetrieveUpdateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class CartView(APIView):
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
