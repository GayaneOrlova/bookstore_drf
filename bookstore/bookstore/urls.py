"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from books.views import BookViewSet
from books.views import GenreListAPIView
from books import views
from books.views import GenreViewSet
from books.views import AuthorListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', BookViewSet.as_view({'get': 'list'})),
    # path("books/", include("books.urls", namespace="books")),
    path('book/<pk>', BookViewSet.as_view({'get': 'retrieve'})),
    path('author/', AuthorListAPIView.as_view(), name='author-list'),
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),

    # path('login', UserLogin.as_view(),)
    path("", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
