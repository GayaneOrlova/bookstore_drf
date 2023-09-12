from django.urls import include, path
from rest_framework.routers import DefaultRouter
from books.models import Book, Genre

from books.views import CommentViewSet


app_name = "books"

router = DefaultRouter()
router.register(r"genre", Genre)
router.register(r"^(?P<book_id>\d+)/comment", CommentViewSet)
router.register(r"", Book)

urlpatterns = [
    path("", include(router.urls)),
]