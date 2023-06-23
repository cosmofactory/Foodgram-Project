from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


MIN_VALUE = 1


class Ingredients(models.Model):
    """Ingredients model."""

    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(verbose_name='единицы измерения')
    slug = models.SlugField(max_length=90)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'Ingredients'


class Tags(models.Model):
    """Tags model."""

    name = models.CharField(max_length=30)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'Tags'


class Recipe(models.Model):
    """Recipe model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Пользователь'
    )
    name = models.CharField(max_length=256)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/',
        max_length=250
    )
    text = models.TextField(verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredients',
        verbose_name='Индгредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipeTags',
        blank=True,
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(MIN_VALUE)]
    )

    def __str__(self):
        return f'{self.author.username} {self.name}'

    class Meta:
        ordering = ('-name',)
        verbose_name_plural = 'Recipes'


class RecipeIngredients(models.Model):
    """Connection model for recipes and ingredients."""

    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_with_ingredient',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredients,
        related_name='ingredient',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_VALUE)]
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_recipe'
            )
        ]


class RecipeTags(models.Model):
    """Connection model for recipes and tags."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_with_tag',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tags,
        related_name='tag',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipe} {self.tag}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_tag'
            )
        ]


class Favorite(models.Model):
    """Favorite model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorited',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]


class ShopCart(models.Model):
    """Shopping cart for recipes."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopcart',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]
