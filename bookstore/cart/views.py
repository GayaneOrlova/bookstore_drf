from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer

class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try: 
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"items": [], "total_price": None})
 
        items = CartItem.objects.filter(cart=cart)
        total_price = sum([item.total_price for item in items])
        serializer = CartItemSerializer(items, many=True)
        return Response({"items": serializer.data, "total_price": total_price})

class UpdateCartItemView(APIView):
    def post(self, request):
        cart_item_id = request.data.get('id')
        amount = request.data.get('amount')
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response("CartItem does not exist", status=status.HTTP_404_NOT_FOUND)

        if amount > 0:
            # cart_item = CartItem.objects.get(id = cart_item_id)
            cart_item.amount = amount
            cart_item.save()
            return Response("ok")
        if amount == 0:
            cart_item = CartItem.objects.get(id = cart_item_id)
            cart_item.delete()
            return Response('delete')
            
        raise RuntimeError("not correct")
