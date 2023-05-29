from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    """Recipe model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Пользователь'
    )
    name = models.CharField(max_length=256)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    text = models.TextField(verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingrediends,
        through='RecipeIngredients',
        verbose_name='Индгредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipeTags',
        blank=True,
        null=True,
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления'
    )