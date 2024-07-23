from rest_framework import serializers

from applications.registration.models import Registration, PossibleAttendees

class PossibleAttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleAttendees
        fields = (
            'id',
            'name',
            'phone',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    possible_attendee = serializers.PrimaryKeyRelatedField(queryset=PossibleAttendees.objects.all())
    whatsapp_number = serializers.CharField(required=False)
    extra_attendees = serializers.IntegerField(required=False, default=0)
    alcohol = serializers.CharField(required=False, default='N')
    weed = serializers.CharField(required=False, default='N')
    vegetarian = serializers.CharField(required=False, default='N')
    is_confirmed = serializers.BooleanField(default=True)
    class Meta:
        model = Registration
        fields = (
            'id',
            'possible_attendee',
            'name',
            'phone',
            'whatsapp_number',
            'extra_attendees',
            'alcohol',
            'weed',
            'vegetarian',
            'is_confirmed',
        )


