from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewset
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser, Follow
from users.serializers import (
    CustomUserSerializer, FollowListSerializer,
    FollowSerializer
)


class UserViewSet(DjoserUserViewset):
    """Viewset for managing Followers"""

    def get(self, request):
        """Get method for users."""
        serializer = CustomUserSerializer(
            self.queryset,
            many=True, data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=False)
    def subscriptions(self, request):
        follow = get_list_or_404(CustomUser, following__user=self.request.user)
        page = self.paginate_queryset(follow)
        serializer = FollowListSerializer(
            page,
            context={'request': request},
            partial=True,
            many=True)
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
