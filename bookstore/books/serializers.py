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
    image = serializers.ImageField()
    ratings = serializers.IntegerField()

    likes = serializers.BooleanField(default=False)
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
    image = serializers.ImageField()
    class Meta:
        model = Comment
        fields = ['book', 'body', 'author', 'image', 'created_at']

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['book', 'body']

class BookRatingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user =CustomUserSerializer
    class Meta:
        model = BookRating
        fields = '__all__'

class BookRatingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ('book', 'rating')


