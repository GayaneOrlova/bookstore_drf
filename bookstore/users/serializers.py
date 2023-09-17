from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")

class UserRegisterationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "password", "confirm_password")
        extra_kwargs = {"password": {"write_only": True}}
        
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data["password"], self.instance)
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return CustomUser.objects.create_user(**validated_data)

    # def create(self, validated_data):
    #     return CustomUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ProfileSerializer(CustomUserSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = ("bio","avatar")

# class ProfileAvatarSerializer(serializers.ModelSerializer):
#     """
#     Serializer class to serialize the avatar
#     """

#     class Meta:
#         model = Profile
#         fields = (,)

# class PasswordChangeSerializer(serializers.Serializer):
#     new_password = serializers.CharField()
#     confirm_password = serializers.CharField()
