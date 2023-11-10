from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import ChangePasswordView
from users import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("me/", views.UserAPIView.as_view(), name="tokens"),
    path("change-userinfo/", views.UserInfoUpdateAPIView.as_view(), name="change_userinfo"),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-avatar/', views.AvatarView.as_view(), name= 'get_avatar'),
    path("avatar/", views.UserAvatarAPIView.as_view(), name="user_avatar"),   
    
    path("tokens/", views.UserTokensFirebase.as_view(), name="user_tokens_firebase"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
