from rest_framework import views
from rest_framework.response import Response

from applications.pokedex import serializers, mixins as pokedex_mixins
from applications.registration import authentication as registration_mixin


class MeViewSet(
    pokedex_mixins.GetProfileFromAuthenticationMixin,
    views.APIView
):
    authentication_classes = [registration_mixin.TokenAuthentication]
    permission_classes = [registration_mixin.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = self.get_profile()
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data)