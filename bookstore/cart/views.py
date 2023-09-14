from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from cart.serializers import CartSerializer

from cart.models import Cart
from rest_framework.response import Response

class CartAPIView(ListCreateAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer(many=True)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
