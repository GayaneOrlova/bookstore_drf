from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ChangePasswordSerializer, ProfileSerializer
from rest_framework.views import APIView

from . import serializers
from .models import Profile

User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = {"user": serializer.data}

        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = {"user": serializer.data}
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

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
            serializer.update(request.user, serializer.validated_data)
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors)

class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserProfileAPIView(RetrieveUpdateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

# class PhotoUploadView(APIView):
#     def post(self, request):
#         file = request.FILES['photo']
#         filename = default_storage.save(file.name, file)
#         return Response({'success': True, 'filename': filename})

class ProfileView(APIView):
    profiles = Profile.objects.get(user_id = 1)
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
        
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.get(user_id = 1)
        serializer = ProfileSerializer(profiles)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):

        file_obj = request.FILES['photo']
        new_data = {"avatar": file_obj}
        serializer = self.serializer_class(self.profiles, data=new_data)
        serializer.is_valid()
        serializer.update(self.profiles, serializer._validated_data)
        # if serializer.is_valid():
            # self.perform_update(serializer)

        return Response(serializer.data)
        # profile_serializer = ProfileSerializer(data=new_data)
        # if profile_serializer.is_valid():
        #     profile_serializer.save()
           
        #     return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     print('error', profile_serializer.errors)
        #     return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
