from users.models import CustomUser
from rest_framework import viewsets, decorators, status
from api.serializers import TagSerializer, RecipeSerializer, RecipeShopcartSerializer, FavoriteSerializer
from recipe.models import Recipe, Ingredients, Tags, Favorite
from users.models import CustomUser, Follow
from shopcart.models import ShopCart
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db import IntegrityError
from django.http import FileResponse
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from rest_framework.exceptions import bad_request
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.decorators import action
from django.http import Http404
from io import BytesIO
from django.core.exceptions import ValidationError
from users.serializers import FollowSerializer
from djoser.views import UserViewSet as DjoserUserViewset
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class UserViewSet(DjoserUserViewset):
    """Viewset for managing Followers"""

  
    @action(detail=False)
    def subscriptions(self, request):
        follow = get_list_or_404(CustomUser, following__user=self.request.user)
        page = self.paginate_queryset(follow)
        serializer = FollowSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    

    @action(detail=True, methods=('post', 'delete'))
    def subscribe(self, request, **kwargs):
        """Adds or removes recipe from user's favorite list."""
        user = self.request.user
        author = get_object_or_404(CustomUser, **kwargs)
        if self.request.method == 'POST':
            if user == author:
                return Response(
                    {"errors": "You can't follow yourself."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            serializer.save(user=user, author=author)
            return Response(serializer.data)
        if self.request.method == 'DELETE':
            try:
                follow = get_object_or_404(
                    Follow,
                    user=user,
                    author=author
                )
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Http404:
                return Response(
                    {"errors": "You are not following this author."},
                    status=status.HTTP_400_BAD_REQUEST
                )


