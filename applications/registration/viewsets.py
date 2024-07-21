from rest_framework import mixins, viewsets

from applications.registration import serializers


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = serializers.RegistrationSerializer
    queryset = serializers.RegistrationSerializer.Meta.model.objects.all()


class PossibleAttendeesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.PossibleAttendeesSerializer
    queryset = serializers.PossibleAttendeesSerializer.Meta.model.objects.all()