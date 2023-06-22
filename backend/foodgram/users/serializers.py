from users.models import User
from djoser.serializers import UserSerializer
from rest_framework.serializers import (
    SerializerMethodField, ModelSerializer, BooleanField
)
from users.models import Follow
from recipe.models import Recipe
from django.core.exceptions import ValidationError
from django.http import Http404


class CustomUserSerializer(UserSerializer):
    """Custom user serializer."""

    is_subscribed = SerializerMethodField()

    class Meta:
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]
        model = User

    def get_is_subscribed(self, obj):
        try:
            user = self.context.get('request').user
            if Follow.objects.filter(user=user.id, author=obj).exists():
                return True
            return False
        except Exception:
            return False


class CreateUserSerializer(UserSerializer):
    """Custom user create serializer."""

    class Meta:
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]
        model = User


class ShortRecipeSerializer(ModelSerializer):
    """Short version of recipe serializer."""

    class Meta:
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
        model = Recipe


class FollowSerializer(CustomUserSerializer):
    """Follow serializer."""

    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]
        model = User

    def get_recipes_count(self, obj):
        counter = User.objects.filter(id=obj.id).values_list(
            'recipes',
            flat=True
        )
        return counter.count()

    def get_recipes(self, obj):
        query_params = self.context.get('request').query_params
        recipes_limit = query_params.get('recipes_limit')
        if recipes_limit is not None:

            recipes = Recipe.objects.filter(author=obj.id)[:int(recipes_limit)]
        else:
            recipes = Recipe.objects.filter(author=obj.id)
        serializer = ShortRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def validate(self, data):
        """Checks if you already follow this user."""
        author = self.instance
        user = self.context.get('request').user
        try:
            if Follow.objects.filter(
                user_id=user.id,
                author_id=author.id
            ).exists():
                raise ValidationError('You are already following this author.')
            return data
        except Http404:
            return data

    def to_internal_value(self, data):
        author = self.instance
        data['email'] = author.email
        data['username'] = author.username
        data['first_name'] = author.first_name
        data['last_name'] = author.last_name
        return data


class FollowListSerializer(FollowSerializer):
    """
    Follow serializer for getting a list of subscriptions.

    This serializer is here because of the errrors with
    is_subscribed field in this particular case. In other
    words, this is KOSTYL'.
    """

    is_subscribed = BooleanField(default=True)

    class Meta:
        fields = FollowSerializer.Meta.fields
        model = User
