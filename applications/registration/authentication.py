from rest_framework.permissions import BasePermission

from applications.registration import models
from rest_framework import authentication, exceptions
from django.utils.translation import gettext_lazy as _


class TokenAuthentication(authentication.TokenAuthentication):
    model = models.AttendeeToken

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('attendee').get(token=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return token.attendee, token


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, models.PossibleAttendees)
