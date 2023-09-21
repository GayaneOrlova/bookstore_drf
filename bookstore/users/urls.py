from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
# from users.views import PhotoUploadView
from users.views import ChangePasswordView
from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("change-username/", views.UserAPIView.as_view(), name="change_username"),
    
    path("me/", views.UserAPIView.as_view(), name="tokens"),

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    # path('avatar/', views.AvatarView.as_view(), name= 'get_avatar'),

    path('change-avatar/', views.AvatarView.as_view(), name= 'get_avatar'),

    path("avatar/", views.UserAvatarAPIView.as_view(), name="user_avatar"),
    # path("profile/change/", views.UserProfileAPIView.as_view(), name="profile-change"),
    # path('avatar/upload/', PhotoUploadView.as_view(), name='photo_upload'),
]
