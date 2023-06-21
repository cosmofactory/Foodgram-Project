from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

v1_router = DefaultRouter()
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('users', UserViewSet)
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
