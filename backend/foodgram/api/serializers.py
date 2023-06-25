import base64

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from recipe.models import (
    Favorite, Ingredients, Recipe, RecipeIngredients,
    RecipeTags, Tags, ShopCart
)
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from api.utils import create_ingredients, create_tags


MIN_VALUE = 1


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
        model = ShopCart
        fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]

    def validate(self, data):
        """Checks if this item is already created."""
        recipe = self.instance
        user = self.context.get('request').user.id
        if self.model.objects.filter(
            user_id=user,
            recipe_id=recipe.id
        ).exists():
            raise ValidationError('Item already in shopcart')
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
    """
    Ingredient serializer for recipe creation.

    Поле id должно быть описано отдельно, чтобы при создании
    рецепта его хватал instance.
    Поле amount нужно для валидации, т.к. валидация модели при
    создании через nested serializers почему то не работает.
    """

    id = serializers.IntegerField()
    amount = serializers.IntegerField(validators=[
        MinValueValidator(MIN_VALUE)
    ])

    class Meta:
        model = RecipeIngredients
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
            request = self.context.get('request')
            user = request.user.id
            return ShopCart.objects.filter(
                user=user,
                recipe_id=obj.id
            ).exists()
        #  Как и просил, обработал именно по частному случаю
        #  При создании рецепта прилетает ошибка KeyError: 'request'
        #  Либо, если через get(), то attirubute error.
        #  Потому что никакого request то не было, мы создавали рецепт
        #  Сделал через get() и часнтный случай, который не влияет
        #  на функциональность обработал.
        except AttributeError:
            return False

    def get_is_favorited(self, obj):
        try:
            request = self.context.get('request')
            user = request.user.id
            return Favorite.objects.filter(
                user=user,
                recipe_id=obj.id
            ).exists()
        except AttributeError:
            return False


class RecipeShopcartSerializer(serializers.ModelSerializer):
    """Shopcart serializer."""

    class Meta:
        #  Модели сделал в соответствии с сериализатором. Я понял про твои
        #  два метода, здесь действительно следующие 40 строчек кода абсолютно
        #  одинаковые, изначально я и пытался этот момент решить через
        #  наследование, не додумавшись до миксина. Из-за того что дедлайн
        #  горит, я сделал как проще но хуже). Потом доработаю этот участок
        #  через миксин, либо через отдельный класс, который заберет и логику
        #  из views.py.
        model = ShopCart
        fields = ['id']

    def validate(self, data):
        """Checks if this item is already created."""
        recipe = self.instance
        user = self.context.get('request').user.id
        if ShopCart.objects.filter(
            user_id=user,
            recipe_id=recipe.id
        ).exists():
            raise ValidationError('Item already in shopcart.')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['name'] = instance.name
        representation['image'] = instance.image.url
        representation['cooking_time'] = instance.cooking_time
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    """Favorite serializer."""

    class Meta:
        model = Favorite
        fields = ['id']

    def validate(self, data):
        """Checks if this item is already created."""
        recipe = self.instance
        user = self.context.get('request').user.id
        if Favorite.objects.filter(
            user_id=user,
            recipe_id=recipe.id
        ).exists():
            raise ValidationError('This recipe is already favorite.')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['name'] = instance.name
        representation['image'] = instance.image.url
        representation['cooking_time'] = instance.cooking_time
        return representation


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
        create_ingredients(RecipeIngredients, ingredients, recipe.id)
        create_tags(RecipeTags, tags, recipe.id)
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
        instance.save()
        recipe = self.data['id']
        RecipeIngredients.objects.filter(recipe_id=self.data['id']).delete()
        RecipeTags.objects.filter(recipe_id=self.data['id']).delete()
        create_ingredients(RecipeIngredients, new_ingredients, recipe)
        create_tags(RecipeTags, new_tags, recipe)
        return instance
