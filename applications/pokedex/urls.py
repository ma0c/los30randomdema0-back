from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.pokedex import viewsets

default_router = DefaultRouter()
default_router.register(r'profile', viewsets.ProfileViewSet, 'profile')
default_router.register(r'pokedex', viewsets.PokedexViewSet, 'pokemon')
default_router.register(r'connection', viewsets.ConnectionViewSet, 'connection')

urlpatterns = [
    path('', include(default_router.urls)),
]