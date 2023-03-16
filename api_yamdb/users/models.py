from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        'First name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Last name',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Biography',
        blank=True
    )

    class UserRoles(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MODERATOR = 'moderator', _('Moderator')
        USER = 'user', _('User')

    role = models.CharField(
        'Role',
        max_length=9,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} is {self.role}'
