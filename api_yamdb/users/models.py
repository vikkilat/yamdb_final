from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель Пользователь."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = [
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модератор')
    ]
    username = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Ник пользователя.',
        help_text='Ник пользователя.'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail.',
        help_text='Адрес электронной почты пользователя.'
    )
    role = models.SlugField(
        choices=ROLES,
        default=USER,
        verbose_name='Роль.',
        help_text='Роль присвоенная пользователю на данном ресурсе.'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Дополнительная информация.',
        help_text='Краткая информация о пользователе.'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя.',
        help_text='Имя пользователя.'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия.',
        help_text='Фамилия пользователя.'
    )
    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Код.',
        help_text='Проверочный код для регистрации на сайте.'
    )

    class Meta:
        verbose_name = 'Пользователь.'
        verbose_name_plural = 'Пользователи.'
        ordering = ['id']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
