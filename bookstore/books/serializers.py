from rest_framework import serializers
from books.models import Book, BookRating, Comment, Genre
from .models import BookFavorite, BookFavorite
from users.serializers import CustomUserSerializer

class BookSerializer(serializers.ModelSerializer):
    title=serializers.CharField()
    author=serializers.CharField()
    genre = serializers.StringRelatedField(many=True)
    published_at=serializers.IntegerField()
    price=serializers.DecimalField(max_digits=5, decimal_places=2)
    available = serializers.BooleanField(default=True)
    recommendation = serializers.BooleanField(default=False)
    new = serializers.BooleanField(default=False)
    bestseller = serializers.BooleanField(default=False)
    image = serializers.ImageField(use_url=True)
    overall_rating = serializers.IntegerField()
    store_amount = serializers.IntegerField()
    like = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BookFavorite.objects.filter(book=obj, user=request.user).exists()
        return False

    def get_comments(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            comments = Comment.objects.filter(book=obj)
            serializer = CommentSerializer(comments, many=True)
            return serializer.data
        return False
    
    def get_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = BookRating.objects.get(book=obj, user=request.user)
                return rating.rating
            except BookRating.DoesNotExist:
                return None
        return None
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


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(required=False )
    avatar_url = serializers.ImageField(required=False )
    body=serializers.CharField()
    class Meta:
        model = Comment
        fields = ['book', 'body', 'author', 'avatar_url', 'created_at']

class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['rating']
        
class BookRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ['book', 'rating']

class BookFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFavorite
        fields = "__all__"

