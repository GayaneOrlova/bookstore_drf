from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from books.models import BookFavorite
from cart.models import  CartItem
from django.db.models import Sum

from .models import Avatar, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    cart_items_books = serializers.SerializerMethodField()
    cart_items_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()

    def get_cart_items_count(self, obj):
        cart_items = CartItem.objects.filter(cart__user=obj).values()
        total_amount = cart_items.aggregate(total_amount=Sum('amount'))['total_amount']
        return total_amount
        
    def get_cart_items_books(self, obj):
        cart_items = CartItem.objects.filter(cart__user=obj).values_list('book_id', flat=True)
        return list(cart_items)
    
    def get_favorites_count(self, obj):
        favorites_count = BookFavorite.objects.filter(user=obj).count()
        return favorites_count
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "cart_items_count", "cart_items_books", "favorites_count")


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
    class Meta:
        model = CustomUser
        fields = ["username"]
      
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