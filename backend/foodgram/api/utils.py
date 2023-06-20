from django_filters import rest_framework as filters
from recipe.models import Recipe


class RecipeFilterSet(filters.FilterSet):
    """Custom filterset for Recipes."""


    is_favorited = filters.BooleanFilter(field_name='favorited')


    #  , method='filter_favorited'
    # def filter_favorited(self, queryset, name, value):
    #     # construct the full lookup expression.
    #     lookup = '__'.join([name, 'isnull'])
    #     return queryset.filter(**{lookup: False})

    #     # alternatively, you could opt to hardcode the lookup. e.g.,
    #     # return queryset.filter(published_on__isnull=False)

    class Meta:
        model = Recipe
        fields = ('author',)


