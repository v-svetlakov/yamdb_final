from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True,
                              error_messages={'unique': 'This email exists'})
    bio = models.TextField(max_length=300, blank=True, null=True)
    confirmation_code = models.CharField(max_length=11)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Roles(models.TextChoices):
        user = 'user', 'Пользователь'
        moderator = 'moderator', 'Модератор'
        admin = 'admin', 'Админ'

    role = models.CharField(
        max_length=12,
        choices=Roles.choices,
        default=Roles.user,
    )

    if role == 'moderator' or role == 'admin':
        is_staff = True
        is_superuser = True

    def __str__(self):
        return self.email