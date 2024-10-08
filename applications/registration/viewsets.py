from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from applications.registration import serializers
from applications.registration.exceptions import AttendeeAlreadyRegisteredException
from applications.registration.models import PossibleAttendees, Registration


class PossibleAttendeesViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.PossibleAttendeesSerializer
    queryset = serializers.PossibleAttendeesSerializer.Meta.model.objects.all()
    lookup_field = 'slug'

    def get_object(self):
        obj = super().get_object()
        try:
            registration = obj.registered_attendee
            raise AttendeeAlreadyRegisteredException(registration)
        except PossibleAttendees.registered_attendee.RelatedObjectDoesNotExist:
            pass
        return obj


class RegistrationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.RegistrationSerializer
    queryset = serializers.RegistrationSerializer.Meta.model.objects.all()
    lookup_field = 'slug'

    @staticmethod
    def validate_possible_attendee_exists(possible_attendee_id):
        return Registration.objects.filter(possible_attendee_id=possible_attendee_id).exists()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.validate_possible_attendee_exists(serializer.validated_data['possible_attendee'].id):
            return Response(
                {'error': 'Possible Attendee already exist, update the existing one instead of creating a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateProfilePicViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.PossibleAttendeeProfilePicSerializer
    queryset = serializers.PossibleAttendeesSerializer.Meta.model.objects.all()
    lookup_field = 'slug'
