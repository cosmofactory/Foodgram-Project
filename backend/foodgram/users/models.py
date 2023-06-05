from django.db import models
from django.contrib.auth.models import AbstractUser


# ROLES = (
#     (USER, 'Пользователь'),
#     (ADMIN, 'Администратор')
# )

class CustomUser(AbstractUser):
    """Reworked User model."""

    email = models.EmailField(
        max_length=254,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    password = models.CharField(
        max_length=150
    )
    is_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
