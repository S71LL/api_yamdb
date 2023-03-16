from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbos_name = 'review'
