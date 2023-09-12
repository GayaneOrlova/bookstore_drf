from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import CustomUser

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)# поменять на ForeinKey(Author)
    genre=models.ManyToManyField(Genre, blank=True)
    created_at=models.DateField(auto_now_add=True)
    price=models.FloatField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    likes = models.ManyToManyField(CustomUser, blank=True)
    body = models.TextField("Book description")

    
    def __str__(self):
        return self.title

class Comment(models.Model):
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="post_comments",
        null=True,
        on_delete=models.SET_NULL,
    )
    body = models.TextField("Comment body")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.author.username}"
