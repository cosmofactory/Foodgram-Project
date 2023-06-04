from users.models import CustomUser
from rest_framework import viewsets
from djoser.views import UserViewSet


# class CustomUserViewSet(UserViewSet):
#     """User viewset."""

#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
