from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TagsViewSet, RecipeViewSet
from users.views import UserViewSet


v1_router = DefaultRouter()
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
