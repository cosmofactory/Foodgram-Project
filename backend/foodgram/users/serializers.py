from users.models import CustomUser
from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField, StringRelatedField, ModelSerializer
from users.models import Follow
from django.db.models import Count
from recipe.models import Recipe
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404


class CustomUserSerializer(UserSerializer):
    """Custom user serializer."""

    class Meta:
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]
        model = CustomUser


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
        model = CustomUser


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

    recipes = ShortRecipeSerializer(many=True, read_only=True)
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
        model = CustomUser

    def get_recipes_count(self, obj):
        counter = CustomUser.objects.filter(id=obj.id).annotate(Count('recipes'))
        return counter[0].recipes__count
    
    def validate(self, data):
        """Checks if this item is already in users cart."""

        author = self.instance
        user = self.context.get('request').user.id
        try:
            if get_object_or_404(Follow, user_id=user, author_id=author.id):
                raise ValidationError('You are already following this author.')
        except Http404:
            return data

    def to_internal_value(self, data):
        author = self.instance
        data['email'] = author.email
        data['username'] = author.username
        data['first_name'] = author.first_name
        data['last_name'] = author.last_name
        return data
