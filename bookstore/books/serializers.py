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
    new = serializers.BooleanField(default=False)
    bestseller = serializers.BooleanField(default=False)
    image = serializers.ImageField(use_url=True)
    overall_rating = serializers.IntegerField()
    store_amount = serializers.IntegerField()
    like = serializers.SerializerMethodField()

    def get_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BookLike.objects.filter(book=obj, user=request.user).exists()
        return False
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
    like = serializers.SerializerMethodField()

    def get_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BookLike.objects.filter(book=obj, user=request.user).exists()
        return False
    
    # def get_avatar(self, obj):
    #     request = self.context.get('request')
    #     image_url = obj.avatar_url
    #     if image_url is not None:
    #         return request.build_absolute_uri(image_url)
    #     return None

    class Meta:
        model = Comment
        fields = ['book', 'body', 'author', 'avatar_url', 'created_at', 'like']

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
    # author = serializers.CharField(source="book.author")
    # title= serializers.CharField(source="book.title")
    # overall_rating = serializers.IntegerField(source="book.overall_rating")
    # id = serializers.IntegerField(source="book.id")
    # price = serializers.DecimalField(source="book.price", max_digits=5, decimal_places=2)
    # image = serializers.SerializerMethodField()
    # available = serializers.BooleanField(source="book.available")
    # new = serializers.BooleanField(source="book.new")
    # bestseller = serializers.BooleanField(source="book.bestseller")
    
    # def get_image(self, obj):
    #     if obj.book.image:
    #         request = self.context.get('request')
    #         if request is not None:
    #             return request.build_absolute_uri(obj.book.image.url)
    #     return None
    class Meta:
        model = BookLike
        # fields = ['price', 'title', 'id', 'image', 'author', 'overall_rating', 'available', 'new', 'bestseller']

        # fields = ['price', 'title', 'id', 'image', 'author', 'overall_rating', 'available', 'new', 'bestseller']
        fields = "__all__"
