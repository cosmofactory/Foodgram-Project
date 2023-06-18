import base64

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from recipe.models import (
    Favorite, Ingredients, Recipe, RecipeIngredients, Tags
)
from rest_framework import serializers
from shopcart.models import ShopCart
from users.serializers import CustomUserSerializer
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class SubscriptionSerializer(serializers.Serializer):
    """Abstract model for serializers that do subscriptions."""
    
    class Meta:
        fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]
    
    def __init__(self, instance=None, data=None, *args, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.error_message = 'This recipe is already in your cart.'
        self.model = ShopCart


    def validate(self, data):
        """Checks if this item is already in users cart."""

        recipe = self.instance
        user = self.context.get('request').user.id
        try:
            if get_object_or_404(self.model, user_id=user, recipe_id=recipe.id):
                raise ValidationError(self.error_message)
        except Http404:
            return data

    def to_internal_value(self, data):
        recipe = self.instance
        data['name'] = recipe.name
        data['cooking_time'] = recipe.cooking_time
        return data


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        model = Tags
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient serializer."""

    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Ingredient-recipe serializer."""

    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    # # amount = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer."""

    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        source='recipe_with_ingredient',
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=True, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
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
        
    def get_is_favorited(self, obj):
        try:
            request = self.context['request']
            user = request.user
            get_object_or_404(Favorite, user=user, recipe_id=obj.id)
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



class RecipeShopcartSerializer(
    SubscriptionSerializer,
    serializers.ModelSerializer
):
    """Shopcart serializer."""

    class Meta:
        model = Recipe
        fields = SubscriptionSerializer.Meta.fields


class FavoriteSerializer(
    SubscriptionSerializer,
    serializers.ModelSerializer
):
    """Favorite serializer."""

    class Meta:
        model = Recipe
        fields = SubscriptionSerializer.Meta.fields

    def __init__(self, instance=None, data=None, *args, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.error_message = 'You are already subscribed to this author.'
        self.model = Favorite
