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

from books.views import AuthorListAPIView, BookRatingUpdateView, BookRatingListCreateView, BookRatingRetrieveUpdateDestroyView, BookViewSet, CommentCreateView, CommentView, GenreListAPIView
from cart.views import AddToCartView, CartAPIView, DeleteFromCartView

urlpatterns = [
    path('admin/', admin.site.urls),
    #  path('api/', include('users.urls')), 
    # path("books/", include("books.urls", namespace="books")),
    path("", include("users.urls", namespace="users")),
    path('all-books/', BookViewSet.as_view({'get': 'list'})),
    path('books/<pk>', BookViewSet.as_view({'get': 'retrieve'})),
    path('authors/', AuthorListAPIView.as_view(), name='author-list'),
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),
    path('books/<int:book_id>/comments/', CommentView.as_view(), name='comment-list-create'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('book-ratings/', BookRatingListCreateView.as_view(), name='book-rating-list-create'),
    path('book-ratings/<int:pk>/', BookRatingRetrieveUpdateDestroyView.as_view(), name='book-rating-retrieve-update-destroy'),
    path('book-ratings/<int:pk>/update/', BookRatingUpdateView.as_view(), name='book-rating-update'),
    
    path('user-cart/', CartAPIView.as_view(), name='user-cart'),
    path('cart/delete-book/', DeleteFromCartView.as_view(), name='cart-item-detail'),
    path('cart/add-book/', AddToCartView.as_view(), name='cart-add'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
