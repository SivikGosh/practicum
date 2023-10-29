import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_username_chars(value):
    er = re.sub(r'[\w.@+-]+', r'', value)
    if len(er) > 0:
        raise ValidationError(
            _(f'Уберите из имени следующее непотребство: {er}'),
            params={'value': value},
        )


class User(AbstractUser):
    username = models.CharField(
        unique=True, max_length=150, verbose_name='логин',
        validators=[validate_username_chars]
    )
    password = models.CharField(
        max_length=150, verbose_name='пароль'
    )
    email = models.EmailField(
        unique=True, max_length=254, verbose_name='почта',
        validators=[EmailValidator(message='Ошибка в email.')]
    )
    first_name = models.CharField(
        max_length=150, verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150, verbose_name='фамилия'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='подписан'
    )

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='user_not_author'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
