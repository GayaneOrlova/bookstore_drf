from books import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from books.models import Book, Genre

from books.views import GenreListAPIView

app_name = "books"

router = DefaultRouter()
router.register(r"genre", Genre)
router.register(r"", Book)

urlpatterns = [
    path("", include(router.urls)),
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),
    

]