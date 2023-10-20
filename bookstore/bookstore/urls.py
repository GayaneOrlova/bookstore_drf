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

from books.views import AuthorListAPIView, BookListAPIView, BookRatingCreateView, BookRatingDetailView, BookViewSet, GenreListAPIView, FavoriteView, FavoriteListView
from books.views import CommentListView
from books.views import CreateCommentView
from books.views import BookRecommendationView
from books.views import SearchAPIView
from cart.views import AddToCartView, CartAPIView, UpdateCartItemView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("users.urls", namespace="users")),
    
    path('all-books/', BookListAPIView.as_view(), name='get-all-book'),
    path('books/<pk>/', BookViewSet.as_view({'get': 'retrieve'})),
    
    path('recommended-books/', BookRecommendationView.as_view(), name='book-list-recommendation'),
    
    path('authors/', AuthorListAPIView.as_view(), name='author-list'),
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),
    
    path('book-comment/<int:book_id>/', CommentListView.as_view(), name='comment-list-create'),
    path('comments/create/', CreateCommentView.as_view(), name='create-comment'),

    path('book-rating/<int:pk>/', BookRatingDetailView.as_view(), name='book_rating'),
    path('book-rating/create/<int:pk>/', BookRatingCreateView.as_view(), name='book_rating'),

    path('cart/', CartAPIView.as_view(), name='user-cart'),
    path('cart-item/update/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),

    path('favorite-change/', FavoriteView.as_view(), name='add-to-favorite'),
    path('favorite-list/', FavoriteListView.as_view(), name='favorite-list'),
    
    # path("api/books/?search=<query>/", SearchAPIView.as_view(), name="search"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
