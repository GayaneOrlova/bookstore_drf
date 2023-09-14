from books import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from books.models import Book, Genre

from books.views import CommentViewSet
from books.views import GenreListAPIView
from bookstore.books.views import AuthorListAPIView


app_name = "books"

router = DefaultRouter()
router.register(r"genre", Genre)
router.register(r"^(?P<book_id>\d+)/comment", CommentViewSet)
router.register(r"", Book)

urlpatterns = [
    path("", include(router.urls)),
    # path('genre/', GenreListAPIView.as_view(), name='genre-list'),
    # path('author/', AuthorListAPIView.as_view(), name='author-list'),

]