from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from account.models import User
from titles.models import Title


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews_title")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="reviews_author")
    text = models.TextField()
    score = models.IntegerField(
        choices=[(x, str(x)) for x in range(1, 11)],
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        "date published",
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="comment_username")
    pub_date = models.DateTimeField(
        "date published",
        auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
