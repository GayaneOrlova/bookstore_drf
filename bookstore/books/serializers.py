from rest_framework import serializers
from books.models import Book, BookRating, Comment, Genre
from users.serializers import CustomUserSerializer

class BookSerializer(serializers.ModelSerializer):
    title=serializers.CharField()
    author=serializers.CharField()
    genre = serializers.StringRelatedField(many=True)
    published_at=serializers.IntegerField()
    price=serializers.DecimalField(max_digits=5, decimal_places=2)
    available = serializers.BooleanField(default=True)
    recommendation = serializers.BooleanField(default=False)
    image = serializers.ImageField(use_url=True)
    overall_rating = serializers.IntegerField()
    store_amount = serializers.IntegerField()

    # likes = serializers.BooleanField(default=False)
    class Meta:
        model = Book
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    class Meta:
        model = Genre
        fields = "__all__"

class AuthorSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    class Meta:
        model = Genre
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    avatar_url = serializers.ImageField()
    class Meta:
        model = Comment
        fields = ['book', 'body', 'author', 'avatar_url', 'created_at']

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['book', 'body']

# class BookRatingSerializer(serializers.ModelSerializer):
#     book = BookSerializer(read_only=True)
#     user =CustomUserSerializer
#     class Meta:
#         model = BookRating
#         fields = '__all__'


class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['rating']
        
class BookRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['book', 'rating']


