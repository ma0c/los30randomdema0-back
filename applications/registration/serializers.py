from rest_framework import serializers

from applications.registration.models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = (
            'name',
            'phone',
            'whatsapp_number',
            'extra_attendees',
            'alcohol',
            'weed',
        )

class PossibleAttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = (
            'name',
            'phone',
            'registered_attendee',
        )