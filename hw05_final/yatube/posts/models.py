""" модели приложения posts """

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class Post(models.Model):
    """ модель поста """

    text = models.TextField(
        verbose_name='Текст', help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации',
        help_text='Дата публикации поста', db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор', help_text='Автор поста'
    )
    group = models.ForeignKey(
        'Group', blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Сообщество', related_name='posts',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField('Картинка', upload_to='posts/', blank=True)
    tag = models.ManyToManyField('Tag', through='TagPost')

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Group(models.Model):
    """ модель группы """

    description = models.TextField(
        verbose_name='Описание', help_text='Описание группы'
    )
    title = models.CharField(
        max_length=200, verbose_name='Имя', help_text='Название группы'
    )
    slug = models.SlugField(
        verbose_name='Адрес', unique=False,
        help_text='Адрес группы в адресной строке'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ модель комментария """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Комментарий', help_text='Комментарий к посту'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор', help_text='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Текст', help_text='Текст комментария'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации',
        help_text='Дата публикации комментария'
    )


class Follow(models.Model):
    """ модель подписки """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик', help_text='Подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор', help_text='Автор'
    )

    class Meta:
        verbose_name = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            ),
            models.CheckConstraint(
                check=~Q(author=F("user")), name='user_not_author'
            )
        ]


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.post}'
