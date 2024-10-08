from django.urls import path, include
from rest_framework import routers

from applications.registration import viewsets

default_router = routers.DefaultRouter()
default_router.register(r'registration', viewsets.RegistrationViewSet, 'registration')
default_router.register(r'possible_attendees', viewsets.PossibleAttendeesViewSet, 'possible_attendees')
default_router.register(r'update_profile_pic', viewsets.UpdateProfilePicViewSet, 'update_profile_pic')


urlpatterns = [
    path('', include(default_router.urls)),
]