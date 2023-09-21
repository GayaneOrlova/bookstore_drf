from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import Avatar, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")

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

    # def create(self, validated_data):
    #     return CustomUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

# class ProfileSerializer(CustomUserSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'


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


# class ProfileSerializer(CustomUserSerializer):
#     class Meta:
#         model = Profile
#         fields = ["bio", "avatar"]
        
class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ["avatar"]
    
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance