from django.db import models
from recipe.models import Recipe
from users.models import CustomUser


class ShopCart(models.Model):
    """Shopping cart for recipes."""

    user = models.ForeignKey(
        CustomUser,
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
