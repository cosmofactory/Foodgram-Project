from users.models import CustomUser
from rest_framework import viewsets, decorators
from api.serializers import TagSerializer, RecipeSerializer, ShopCartSerializer, RecipeShopcartSerializer
from recipe.models import Recipe, Ingredients, Tags, Follow
from shopcart.models import ShopCart
from django.shortcuts import get_object_or_404



class TagsViewSet(viewsets.ModelViewSet):
    """Viewset for Tags."""

    serializer_class = TagSerializer
    queryset = Tags.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipes."""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class ShopCartViewSet(viewsets.ModelViewSet):
    """Viewset for Shop cart."""

    queryset = ShopCart.objects.all()
    serializer_class = ShopCartSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            Recipe, id=self.kwargs['recipe_id']
        )
        serializer.save(user=self.request.user, recipe=recipe)

