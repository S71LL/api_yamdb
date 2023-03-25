from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'category'

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=200, default='empty')
    year = models.IntegerField(default=2000)
    rating = models.FloatField(null=True, default=None)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title',
    )

    class Meta:
        verbose_name = 'title'

    def __str__(self) -> str:
        return self.name

    def get_rating(self):
        return Review.objects.filter(title_id=self.id).aggregate(Avg('score'))


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'genre'

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Title'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Genre'
    )

    class Meta:
        verbose_name = 'title and genre'
        verbose_name_plural = 'titles and genres'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'review'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


'''class ReviewComment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment'
    )


class TitleReview(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Review'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Title'
    )
'''
