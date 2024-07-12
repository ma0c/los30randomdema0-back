from rest_framework import mixins, viewsets

from applications.registration import serializers


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.RegistrationSerializer
    queryset = serializers.RegistrationSerializer.Meta.model.objects.all()
