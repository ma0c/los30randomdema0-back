from django.urls import path, include
from rest_framework import routers

from applications.registration import viewsets

default_router = routers.DefaultRouter()
default_router.register(r'registration', viewsets.RegistrationViewSet)


urlpatterns = [
    path('', include(default_router.urls)),
]