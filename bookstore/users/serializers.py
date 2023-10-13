from ipaddress import summarize_address_range
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from cart.models import  CartItem, Cart
from django.db.models import Sum


from .models import Avatar, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    cart_items_count = serializers.SerializerMethodField()

    def get_cart_items_count(self, obj):
        cart_items = CartItem.objects.filter(cart__user=obj).values()
        print(cart_items, 'cart_items')
        total_amount = cart_items.aggregate(total_amount=Sum('amount'))['total_amount']

        return total_amount
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "cart_items_count")



    # cart_items_count = serializers.SerializerMethodField()
    # def get_cart_items_count(self, obj):
    #     return CartItem.objects.filter(cart__user=obj).count()

    # # cart = serializers.SerializerMethodField()

    # # def get_cart(self, obj):
    # #     request = self.context.get('request')
    # #     if request and request.user.is_authenticated:
    # #         return Cart.objects.get(cart=obj, user=request.user)
    # #     return False

    # class Meta:
    #     model = CustomUser
    #     fields = ("id", "username", "email", "get_cart_items_count")

class UserRegisterationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = CustomUser
        fields = ("id", "email", 'username', "password", "confirm_password")
        extra_kwargs = {"password": {"write_only": True}}
        
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data["password"], self.instance)
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return CustomUser.objects.create_user(**validated_data)
        
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        if not self.context['request'].user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect password")

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance   

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["avatar"]
    
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance