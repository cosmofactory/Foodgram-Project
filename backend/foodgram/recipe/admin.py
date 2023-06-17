from django.contrib import admin
from recipe.models import (
    Ingredients,
    Tags,
    Recipe,
    RecipeIngredients,
    RecipeTags,
    Favorite
)


class RIInline(admin.TabularInline):
    """Recipe - Ingredients table relation."""

    model = RecipeIngredients
    extra = 1


class RTInline(admin.TabularInline):
    """Recipe - Tags table relation."""

    model = RecipeTags
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """Admin for RIInline."""

    inlines = [RIInline, RTInline]
    list_display = ['name', 'author', ]
    list_filter = ['author', 'name', 'tags', ]


class IngredientsAdmin(admin.ModelAdmin):
    """Admin for RIInline."""

    inlines = [RIInline, ]
    list_display = ['name', 'measurement_unit', ]
    list_filter = ['name', ]


class TagsAdmin(admin.ModelAdmin):
    """Admin for RTInline"""

    inlines = [RTInline, ]


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
