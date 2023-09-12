from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from cart.serializers import CartSerializer

from cart.models import Cart


class CartAPIView(ListCreateAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer

