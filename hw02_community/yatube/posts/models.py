"""Модели приложения Posts"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Модель поста"""

    text = models.TextField(verbose_name='Текст')

    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор')

    group = models.ForeignKey('Group',
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Сообщество',
                              related_name='posts')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class Group(models.Model):
    """Модель сообщества"""

    description = models.TextField(verbose_name='Описание')

    title = models.CharField(max_length=200,
                             verbose_name='Имя')

    slug = models.SlugField(verbose_name='Адрес',
                            unique=True)

    def __str__(self):
        return self.title
