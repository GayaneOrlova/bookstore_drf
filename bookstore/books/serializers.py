from rest_framework import serializers
from books.models import Book, BookRating, Comment, Genre
from .models import BookLike
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
        fields = ['body']

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['rating']
        
class BookRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['book', 'rating']

class BookLikeSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="book.author")
    title= serializers.CharField(source="book.title")
    overall_rating = serializers.IntegerField(source="book.overall_rating")
    id = serializers.IntegerField(source="book.id")
    price = serializers.DecimalField(source="book.price", max_digits=5, decimal_places=2)
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj):
        if obj.book.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.book.image.url)
        return None
    class Meta:
        model = BookLike
        fields = ['price', 'title', 'id', 'image', 'author', 'overall_rating']
