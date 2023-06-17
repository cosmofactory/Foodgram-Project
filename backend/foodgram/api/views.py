from users.models import CustomUser
from rest_framework import viewsets, decorators, status
from api.serializers import TagSerializer, RecipeSerializer, ShopCartSerializer, RecipeShopcartSerializer
from recipe.models import Recipe, Ingredients, Tags, Follow
from shopcart.models import ShopCart
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.exceptions import bad_request
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.decorators import action
import sys




class TagsViewSet(viewsets.ModelViewSet):
    """Viewset for Tags."""

    serializer_class = TagSerializer
    queryset = Tags.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipes."""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


    @action(detail=True, methods=('post', 'delete'), url_path='shopping_cart')
    def shopping_cart(self, request, **kwargs):
        user = self.request.user.id
        recipe = get_object_or_404(Recipe, **kwargs)
        if self.request.method == 'POST':
            serializer = RecipeShopcartSerializer(recipe, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            ShopCart.objects.create(user_id=user, recipe=recipe)
            serializer.save(id=user, recipe=recipe)
            return Response(serializer.data)



class ShopCartViewSet(ModelViewSet):
    """Viewset for Shop cart."""

    queryset = ShopCart.objects.all()
    serializer_class = ShopCartSerializer


    def perform_create(self, serializer):
        recipe = get_object_or_404(
            Recipe, id=self.kwargs['recipe_id']
        )          
        serializer.save(user=self.request.user, recipe=recipe)
    
    @action(detail=True, methods=['delete'])
    def perform_destroy(self, instance):
        instance = get_object_or_404(ShopCart, user=self.request.user, recipe=self.kwargs['recipe'])
        instance.delete()
        

