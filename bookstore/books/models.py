import datetime
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from users.models import Avatar

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
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    genre=models.ManyToManyField(Genre, blank=True)
    published_at=models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(datetime.date.today().year)])
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)
    likes = models.ManyToManyField(CustomUser, blank=True, related_name="likes")
    body = models.TextField("Book description")

    @property
    def overall_rating(self):
        ratings = BookRating.objects.all().filter(book=self.id)
        if len(ratings) > 0:
            return sum([x.rating for x in ratings]) / len(ratings)
        else:
            return 0
    ratings = overall_rating
    
    def __str__(self):
        return self.title
        
        
class Comment(models.Model):
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField("Comment body")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=False, blank=False)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:10]} by User {self.user.username}"
        
    def author(self):
        author = self.user.username
        return author
        
    def image(self):
        image = self.avatar.avatar
        return image


class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)    

    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f"Book {self.book.title} rated {self.rating} by User {self.user.username}"