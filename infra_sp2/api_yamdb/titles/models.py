from django.db import models


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug',
        help_text='Адрес категории в адресной строке'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug',
        help_text='Адрес жанра в адресной строке'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        help_text='Год выпуска произведения'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория произведения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']


class GenreTitle(models.Model):
    """Связующая жанры с произведениями модель."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.title} - {self.genre}'

    class Meta:
        verbose_name = 'Жанр - Произведение'
        verbose_name_plural = 'Жанры - Произведения'
        ordering = ['-id']
