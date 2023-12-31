from ast import List
from http.client import responses
from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AvatarSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
import firebase_admin
from firebase_admin import messaging
from bookstore.settings import AUTH_USER_MODEL
from firebase_admin import messaging

from . import serializers
from .models import Avatar, CustomUser, DeviceTypes, UserDevice

User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            token = RefreshToken.for_user(user)
            data = {"user": serializer.data}

            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error = e.detail
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            serializer = serializers.CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = {"user": serializer.data}
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


class UserTokensFirebase(GenericAPIView):
    def post(self, request, *args, **kwargs):
            firebase_token = request.data["fcmToken"]
            token = request.auth
            user = CustomUser.objects.get(id = token['user_id'])
            UserDevice.objects.get_or_create(type=DeviceTypes.ANDROID, user= user, firebase_token = firebase_token)
            
            return Response(status=status.HTTP_200_OK)
    

class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if not request.user.check_password(serializer.validated_data.get('password')):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(request.user, serializer.validated_data)
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserInfoUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserUpdateSerializer

    def get_object(self):
        return self.request.user

class UserAvatarAPIView(RetrieveUpdateAPIView):
    queryset = Avatar.objects.all()
    serializer_class = serializers.AvatarSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.avatar
        
class AvatarView(APIView):
    serializer_class = AvatarSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
   
    def patch(self, request):
        avatar = Avatar.objects.get(user=request.user)
        file_obj = request.FILES['photo']
        new_data = {"avatar": file_obj}
        serializer = self.serializer_class(avatar, data=new_data)
        serializer.is_valid()
        serializer.update(avatar, serializer._validated_data)
        return Response(serializer.data)