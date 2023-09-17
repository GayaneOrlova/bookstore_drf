from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import ChangePasswordView

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    path("profile/change/", views.UserProfileAPIView.as_view(), name="profile-change"),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path("me/", views.UserAPIView.as_view(), name="tokens"),
]
