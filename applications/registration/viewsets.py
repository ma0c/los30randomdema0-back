from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from applications.registration import serializers


class PossibleAttendeesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.PossibleAttendeesSerializer
    queryset = serializers.PossibleAttendeesSerializer.Meta.model.objects.all()


class RegistrationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.RegistrationSerializer
    queryset = serializers.RegistrationSerializer.Meta.model.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


