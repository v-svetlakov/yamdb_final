from django.db import models
from django.db.models import Avg


class Categories(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=50)
    year = models.IntegerField("Год выпуска")
    description = models.TextField(max_length=200)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Categories, 
        on_delete=models.SET_NULL, 
        related_name="category_titles", 
        null=True, 
        blank=True
    )

    @property
    def rating(self):
        value = self.reviews_title.all().aggregate(
            Avg('score')).get('score__avg')
        if value:
            return round(value, 1)
        return None

    def __str__(self):
        return self.name
