"""Модели приложения Posts"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Модель поста"""

    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст нового поста'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации поста'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста'
    )

    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Сообщество',
        related_name='posts',
        help_text='Группа, к которой будет относиться пост'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Group(models.Model):
    """Модель сообщества"""

    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание группы'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='Имя',
        help_text='Название группы'
    )

    slug = models.SlugField(
        verbose_name='Адрес',
        unique=True,
        help_text='Адрес группы в адресной строке'
    )

    def __str__(self):
        return self.title
