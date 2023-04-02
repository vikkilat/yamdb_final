import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

YEAR = datetime.datetime.now().year


class Category(models.Model):
    """Модель Категория."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Категория.',
        help_text='Категория к которой относится произведение.'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес категории.',
        help_text='Имя категории для формирования url.'
    )

    class Meta:
        verbose_name = 'Категория.'
        verbose_name_plural = 'Категории.'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Жанр."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Жанр.',
        help_text='Жанр, к которому относятся произведения.'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес жанра.',
        help_text='Имя жанра для формирования url.'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры.'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Произведение."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Произведение.',
        help_text='Название произведения.'
    )
    year = models.IntegerField(
        verbose_name='Год.',
        help_text='Год создания произведения',
        validators=(MaxValueValidator(limit_value=YEAR),)
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name='Описание.',
        help_text='Описание произведения.',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория.',
        help_text='Категория произведения.'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр.',
        help_text='Жанры, к которым относится произведение.'
    )

    class Meta:
        verbose_name = 'Произведение.'
        verbose_name_plural = 'Произведения.'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение.',
        help_text='Произведение, на которое написан отзыв.'
    )
    text = models.TextField(verbose_name='Текст отзыва.')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь.',
        help_text='Автор отзыва.'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        null=True,
        verbose_name='Рейтинг.',
        help_text='Оценка произведения пользователем (от 1 до 10 баллов.)'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата.',
        help_text='Дата публикации отзыва.'
    )

    class Meta:
        verbose_name = 'Отзыв.'
        verbose_name_plural = 'Отзывы.'
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель Комментария к отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв.',
        help_text='Отзыв о произведении к которому относится комментарий.'
    )
    text = models.TextField(
        verbose_name='Текст комментария.',
        help_text='Текст комментария.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь.',
        help_text='Автор комментария.'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата.',
        help_text='Дата публикации комментария.',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Комментарии.'
        verbose_name = 'Комментарий.'

    def __str__(self):
        return self.text
