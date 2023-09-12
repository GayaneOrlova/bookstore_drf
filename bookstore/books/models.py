from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
    def __str__(self):
        return self.title
  