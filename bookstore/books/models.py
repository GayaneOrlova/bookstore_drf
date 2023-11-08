import datetime
from typing import Any
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Avatar, CustomUser
from django.core.exceptions import ObjectDoesNotExist

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
    recommendation = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)
    body = models.TextField("Book description")
    
    @property
    def overall_rating(self):
        ratings = BookRating.objects.all().filter(book=self.id)
        if len(ratings) > 0:
            return sum([x.rating for x in ratings]) / len(ratings)
        else:
            return 0
    
    def __str__(self):
        return self.title   
    
class Comment(models.Model):
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField("Comment body")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    class Meta:
        ordering = ("-created_at",)
        
    @property
    def avatar_url(self):
        try:
            avatar = Avatar.objects.get(user=self.user)
        except ObjectDoesNotExist:
            return None
        return avatar.avatar

    def __str__(self):
        return f"{self.body[:10]} by User {self.user.username}"
        
    @property    
    def author(self):
        author = self.user.username
        return author
         
    def formatted_date(self):
        time_diff = timezone.now() - self.created_at

        if time_diff < timezone.timedelta(minutes=60):
            minutes = int(time_diff.total_seconds() // 60)
            return f"Left a comment {minutes} minutes ago"
        elif time_diff < timezone.timedelta(days=1):
            hours = int(time_diff.total_seconds() // 3600)
            return f"Left a comment {hours} hours ago"
        else:
            days = int(time_diff.total_seconds() // (24 * 3600))
            return f"Left a comment {days} days ago"

class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])    
    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f"Book {self.book.title} rated {self.rating} by User {self.user.username}"

class BookFavorite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=True)
    
