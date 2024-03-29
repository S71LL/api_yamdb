from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MODERATOR = 'moderator', _('Moderator')
        USER = 'user', _('User')

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        validators=[ASCIIUsernameValidator],
        db_index=True
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True
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
    role = models.CharField(
        'Role',
        max_length=9,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    confirmation_code = models.CharField(
        'Confirmation_code',
        max_length=100,
        blank=True
    )
    token = models.CharField(
        'Token',
        max_length=254,
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.role} {self.username}'
