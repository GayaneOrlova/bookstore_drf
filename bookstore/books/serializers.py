from rest_framework import serializers
from books.models import Book, BookRating, Comment, Genre
from .models import BookFavorite, BookFavorite

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
    rating = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BookFavorite.objects.filter(book=obj, user=request.user).exists()
        return False

    def get_comments(self, obj):
        request = self.context.get('request')
        if request:
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
    formatted_date = serializers.CharField()
    
    class Meta:
        model = Comment
        fields = ['book', 'body', 'author', 'avatar_url', 'formatted_date']


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(required=False )
    avatar_url = serializers.ImageField(required=False )
    body=serializers.CharField()
    class Meta:
        model = Comment
        fields = ['book', 'body', 'author', 'avatar_url', 'created_at', 'formatted_date']

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

class FavoriteListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="book.title")
    author = serializers.CharField(source="book.author")
    id = serializers.IntegerField(source="book.id")
    price = serializers.DecimalField(source="book.price", max_digits=5, decimal_places=2)
    overall_rating = serializers.DecimalField(source="book.overall_rating", max_digits=5, decimal_places=2)
    image = serializers.SerializerMethodField()
    available = serializers.BooleanField(source="book.available")
    like = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.book.image.url
        return request.build_absolute_uri(image_url)
        
    def get_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BookFavorite.objects.filter(book=obj.book, user=request.user).exists()
        return False

    class Meta:
        model = BookFavorite
        fields = ['price', 'title', 'id', 'image', "author", "overall_rating", "available", "like"]
        