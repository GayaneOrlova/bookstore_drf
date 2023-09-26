from rest_framework import serializers

from books.models import Book
from books.models import Genre
from books.models import Comment
from books.models import BookRating

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
        # read_only_fields = ('overall_rating',)

        
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

class CommentReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

class CommentWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = "__all__"


class BookRatingSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = BookRating
    #     fields = ['id', 'book', 'user', 'rating']
    book = BookSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = BookRating
        fields = '__all__'


class BookRatingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRating
        fields = ('book', 'rating')


