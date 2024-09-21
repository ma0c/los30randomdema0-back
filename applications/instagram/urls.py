from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.instagram import viewsets

default_router = DefaultRouter()
default_router.register(r'photos', viewsets.PhotoViewSet, 'photos')


urlpatterns = [
    path('', include(default_router.urls)),
]