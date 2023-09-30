from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE, default=1)
    location = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    is_offered = models.BooleanField(default=False)
    interested_users = models.ManyToManyField(User, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title
