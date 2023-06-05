from django.db import models
from users.models import CustomUser
from recipe.models import Recipe


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
