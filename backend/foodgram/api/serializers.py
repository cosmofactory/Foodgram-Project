import base64

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from recipe.models import (
    Favorite, Ingredients, Recipe, RecipeIngredients, Tags, RecipeTags
)
from rest_framework import serializers
from shopcart.models import ShopCart
from users.serializers import CustomUserSerializer


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
            if get_object_or_404(
                self.model, user_id=user, recipe_id=recipe.id
            ):
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


# class TagRecipeSerializer(serializers.StringRelatedField):
#     """Tag recipe creation serializer."""

#     class Meta:
#         model = RecipeTags
#         fields = '__all__'

#     def to_internal_value(self, data):
#         tag_id = data['id']
#         RecipeTags.objects.create()
#         return data


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient serializer."""

    id = serializers.IntegerField()
    amount = serializers.FloatField()

    class Meta:
        model = Ingredients
        fields = ['id', 'amount']


class IngredientViewSerializer(serializers.ModelSerializer):
    """Ingredient view serializer."""

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
            user = request.user.id
            get_object_or_404(ShopCart, user=user, recipe_id=obj.id)
            return True
        except Exception:
            return False

    def get_is_favorited(self, obj):
        try:
            request = self.context['request']
            user = request.user.id
            get_object_or_404(Favorite, user=user, recipe_id=obj.id)
            return True
        except Exception:
            return False


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


class RecipeCreationSerializer(serializers.ModelSerializer):
    """Serializer for creating recipe."""

    ingredients = IngredientSerializer(
        many=True
    )
    tags = serializers.SlugRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        slug_field='id'
    )
    image = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = Recipe
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        ]

    def to_representation(self, value):
        serializer = RecipeSerializer(value)
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')
            RecipeIngredients.objects.create(
                ingredient_id=ingredient_id,
                recipe=recipe,
                amount=amount
            )
        for tag in tags:
            RecipeTags.objects.create(tag=tag, recipe=recipe)
        return recipe

    def update(self, instance, validated_data):
        new_ingredients = validated_data.pop('ingredients')
        new_tags = validated_data.pop('tags')

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.set(new_tags)
        # new_list = []
        # for ingredient in new_ingredients:
        #     obj = get_object_or_404(Ingredients, id=ingredient.get('id'))
        #     new_list.append(obj)
        #     # instance.ingredients.set(obj)
        #     # instance.ingredients.amount.add(ingredient.get('amount'))
        #     # instance.save()
        # instance.ingredients.set(new_list)
        instance.save()

        new_ingredients_id_list = []
        old_ingredients = RecipeIngredients.objects.filter(
            recipe_id=self.data['id']
        )
        for new in new_ingredients:
            # Updating or creating existing DB objects
            ingredient_id = new.get('id')
            ingredient_amount = new.get('amount')
            # Getting a list of new id's for further use
            new_ingredients_id_list.append(ingredient_id)
            RecipeIngredients.objects.update_or_create(
                ingredient_id=ingredient_id,
                recipe_id=self.data['id'],
                defaults={'amount': ingredient_amount}
            )

        for old in old_ingredients:
            # deleting removed ingredients from recipe
            if old.ingredient_id not in new_ingredients_id_list:
                RecipeIngredients.objects.filter(id=old.id).delete()

        new_tags_id_list = []
        old_tags = RecipeTags.objects.filter(
            recipe_id=self.data['id']
        )
        for new in new_tags:
            # Updating or creating existing DB objects
            # Getting a list of new id's for further use
            new_tags_id_list.append(new.id)
            RecipeTags.objects.update_or_create(
                tag_id=new.id,
                recipe_id=self.data['id'],
            )

        for old in old_tags:
            # deleting removed ingredients from recipe
            if old.tag_id not in new_tags_id_list:
                RecipeTags.objects.filter(id=old.id).delete()
        return instance
