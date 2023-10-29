from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.html import mark_safe
from foodgram.settings import MEDIA_URL
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = models.CharField(
        'Цвет',
        null=True,
        max_length=7,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})', message='Укажите HEX-код нужного цвета.'
            )
        ]
    )
    slug = models.SlugField('Slug', unique=True, null=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


# не стал добавлять slug, оставил id, как указано в Redoc
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipe_images/'
    )
    text = models.TextField(
        'Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe(
            f'<img src="{MEDIA_URL}{self.image}" width="99" height="99">'
        )

    image_tag.short_description = 'Фото готового блюда'
    image_tag.allow_tags = True


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        'Количество', validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Количества ингредиентов'
        verbose_name_plural = 'Количества ингредиентов'
        constraints = [
            models.UniqueConstraint(
                name='unique_combination', fields=['recipe', 'ingredient']
            )
        ]

    def __str__(self):
        return (
            f'{self.recipe.name}: '
            f'{self.ingredient.name} - '
            f'{self.amount} '
            f'{self.ingredient.measurement_unit}'
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Избранный автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                name='unique_favorite', fields=['user', 'recipe']
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_user'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_recipe'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                name='unique_shopping_cart', fields=['user', 'recipe'],
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
