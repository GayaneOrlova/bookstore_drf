import datetime
from typing import Any
from django.db import models
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
# class BookStatus(models.Model):
#     available = models.BooleanField(default=True)
#     store_amount = models.IntegerField(default=1)#
#     book=models.ForeignKey("Book", on_delete=models.CASCADE)

# class BookModelManager(models.Manager):
#     def create(self, **kwargs: Any) -> Any:
#         book= super().create(**kwargs)
#         BookStatus.objects.create(book=book)
#         return book

class Book(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    genre=models.ManyToManyField(Genre, blank=True)
    published_at=models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(datetime.date.today().year)])
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    recommendation = models.BooleanField(default=False)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)
    # likes = models.ManyToManyField(CustomUser, blank=True, related_name="likes")
    body = models.TextField("Book description")
    store_amount = models.IntegerField(default=1)#
    
    
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
    updated_at = models.DateTimeField(auto_now=True)
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
        
    def author(self):
        author = self.user.username
        return author

class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])    
    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f"Book {self.book.title} rated {self.rating} by User {self.user.username}"

class BookLike(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=True)
    