from django.db import models
from django.contrib.auth import get_user_model

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     pass

User = get_user_model()
# Временное решение, пока не напишу модель юзера


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title',
    )


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        related_name='review'
    )


class Comments(models.Model):
    text = models.CharField(max_length=200)
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True
    )
