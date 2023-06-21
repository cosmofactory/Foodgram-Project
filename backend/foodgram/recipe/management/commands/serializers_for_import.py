from recipe.models import Ingredients
from rest_framework.serializers import ModelSerializer


class IngredientSerializer(ModelSerializer):
    """Serializer for csv import."""

    class Meta:
        model = Ingredients
        fields = ['name', 'measurement_unit']
