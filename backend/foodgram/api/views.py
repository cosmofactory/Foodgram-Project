from io import BytesIO

from api.serializers import (
    FavoriteSerializer, RecipeSerializer, RecipeShopcartSerializer,
    TagSerializer, RecipeCreationSerializer,
    IngredientViewSerializer
)
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from recipe.models import Favorite, Ingredients, Recipe, Tags
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from shopcart.models import ShopCart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for Tags."""

    serializer_class = TagSerializer
    queryset = Tags.objects.all()
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for Ingredients."""

    serializer_class = IngredientViewSerializer
    queryset = Ingredients.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = None
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipes."""

    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'tags__slug']

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all().annotate(
        ).prefetch_related(
            'ingredients',
            'tags',
            'author'
        ).order_by('name')
        favorited = self.request.query_params.get('is_favorited')
        if favorited == '1':
            queryset = queryset.filter(favorited__user_id=user.id)
        in_shop_cart = self.request.query_params.get('is_in_shopping_cart')
        if in_shop_cart == '1':
            queryset = queryset.filter(shopcart__user_id=user.id)

        tags = self.request.query_params.getlist('tags')
        if not not tags:
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreationSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, **kwargs):
        """Adds or removes recipe from user's shopping list."""
        user = self.request.user.id
        recipe = get_object_or_404(Recipe, **kwargs)
        if self.request.method == 'POST':
            serializer = RecipeShopcartSerializer(
                recipe,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            ShopCart.objects.create(user_id=user, recipe=recipe)
            serializer.save(id=user, recipe=recipe)
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            try:
                shop_cart = get_object_or_404(
                    ShopCart,
                    user=user,
                    recipe=recipe
                )
                shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                return Response(
                    {"errors": "You dont have this recipe in your shopcart."},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Download user's shopcart."""

        information = ShopCart.objects.filter(
            recipe__shopcart__user=self.request.user.id
        )
        buffer = BytesIO()
        file = canvas.Canvas(buffer)
        file.drawString(100, 100, str(information))
        file.showPage()
        file.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping_cart.pdf'
        )

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, **kwargs):
        """Adds or removes recipe from user's favorite list."""
        user = self.request.user.id
        recipe = get_object_or_404(Recipe, **kwargs)
        if self.request.method == 'POST':
            serializer = FavoriteSerializer(
                recipe,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(user_id=user, recipe=recipe)
            serializer.save(id=user, recipe=recipe)
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            try:
                shop_cart = get_object_or_404(
                    Favorite,
                    user=user,
                    recipe=recipe
                )
                shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                return Response(
                    {"errors": "This recipe is not in your favorites."},
                    status=status.HTTP_400_BAD_REQUEST
                )
