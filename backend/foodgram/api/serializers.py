from rest_framework import serializers
from recipe.models import Recipe, Tags, Ingredients, Follow, RecipeIngredients
from users.serializers import CustomUserSerializer
from shopcart.models import ShopCart
import base64
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        model = Ingredients
        fields = '__all__'
        model = Tags


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient serializer."""

    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Ingredient-recipe serializer."""

    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer."""

    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=True, allow_null=True)
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_is_in_shopping_cart(self, obj):
        try:
            request = self.context['request']
            user = request.user
            get_object_or_404(ShopCart, user=user, recipe_id=obj.id)
            return True
        except Http404:
            return False


class RecipeCreationSerializer(serializers.ModelSerializer):
    """Recipe creation serializer."""

    ingredients = serializers.SlugRelatedField(
        slug_field='slug', queryset=Ingredients.objects.all(), required=True
    )
    tags = serializers.SlugRelatedField(
        slug_field='slug', queryset=Tags.objects.all(), required=True
    )

    class Meta:
        model = Recipe
        fields = [
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        ]


class RecipeShopcartSerializer(serializers.ModelSerializer):
    """Adding to shopcart serializer."""

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]


class ShopCartSerializer(serializers.ModelSerializer):
    """Shop cart serializer."""

    class Meta:
        model = ShopCart
        fields = ['user', 'recipe']


    def validate(self, data):
        """Checks if this item is already in users cart."""


        request = self.context['request']
        user = request.user.id
        recipe = self.context.get('view').kwargs.get('recipe_id')
        try:
            if get_object_or_404(ShopCart, user=user, recipe=recipe):
                raise ValidationError('This recipe is already in your cart.')
        except Http404:

            return data



    def to_representation(self, instance):
        """Returns some recipe information after successful adding."""
        recipe = get_object_or_404(Recipe, id=instance.recipe.id)
        serializer = RecipeShopcartSerializer(recipe)
        return serializer.data
