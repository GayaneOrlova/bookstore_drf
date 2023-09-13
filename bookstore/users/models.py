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
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

def get_image_filename(instance, filename):
    name = instance
    slug = slugify(name)
    return f"books/{slug}-{filename}"

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')


        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_image_filename, blank=True)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def filename(self):
        return os.path.basename(self.image.name)