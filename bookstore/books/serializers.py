from rest_framework import serializers

from books.models import Book
from books.models import Genre
from books.models import Comment

class BookSerializer(serializers.ModelSerializer):
    title=serializers.CharField()
    author=serializers.CharField()
    genre=serializers.CharField() 
    created_at=serializers.DateField()
    price=serializers.FloatField()
    available = serializers.BooleanField(default=True)
    image = serializers.ImageField()
    rating = serializers.IntegerField()
    likes = serializers.BooleanField(default=False)
    
    class Meta:
        model = Book
        fields = "__all__"
        
        
class GenreSerializer(serializers.ModelSerializer):
    name=serializers.CharField()

class AuthorSerializer(serializers.ModelSerializer):
    name=serializers.CharField()

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