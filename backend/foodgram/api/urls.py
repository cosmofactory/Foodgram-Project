from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views



# from api.views import (

# )

v1_router = DefaultRouter()
# v1_router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    # path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
