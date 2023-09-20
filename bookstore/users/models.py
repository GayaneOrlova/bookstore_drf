from django.contrib.auth.models import AbstractUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
import os

# from users.serializers import PasswordChangeSerializer
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, blank=True)
    # bio = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return self.username

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

def get_image_filename(instance, filename):
    name = instance
    slug = slugify(name)
    return f"avatars/{slug}-{filename}"

    # def post(self, request):
    #     serializer = PasswordChangeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     password = request.data.get('password')
    #     new_password = serializer.validated_data['new_password']
    #     confirm_password = serializer.validated_data['confirm_password']
        
    #     if new_password != confirm_password:
    #         return Response({'error': 'Passwords do not match'}, status=400)
        
    #     user = request.user 
    #     user.set_password(new_password)
    #     user.save()
        
    #     return Response({'message': 'Password changed successfully'})



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_image_filename)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def filename(self):
        return os.path.basename(self.image.name)