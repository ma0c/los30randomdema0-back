from rest_framework import views
from rest_framework.response import Response

from applications.pokedex import serializers, mixins as pokedex_mixins
from applications.registration.mixins import IsAuthenticatedAppMixin


class MeViewSet(
    IsAuthenticatedAppMixin,
    pokedex_mixins.GetProfileFromAuthenticationMixin,
    views.APIView
):


    def get(self, request, *args, **kwargs):
        profile = self.get_profile()
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data)