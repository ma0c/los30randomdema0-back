from rest_framework import serializers

from applications.registration.models import Registration, PossibleAttendees


class PossibleAttendeesSerializer(serializers.ModelSerializer):
    registered_attendee = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = PossibleAttendees
        fields = (
            'id',
            'name',
            'phone',
            'instagram',
            'profile_pic',
            'registered_attendee',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    possible_attendee = serializers.PrimaryKeyRelatedField(queryset=PossibleAttendees.objects.all())
    whatsapp_number = serializers.CharField(required=False)
    extra_attendees = serializers.IntegerField(required=False, default=0)
    alcohol = serializers.CharField(required=False, default='N')
    weed = serializers.CharField(required=False, default='N')
    vegetarian = serializers.CharField(required=False, default='N')
    entry_hour = serializers.DateTimeField(required=False)
    exit_hour = serializers.DateTimeField(required=False)
    is_confirmed = serializers.BooleanField(default=True)

    def validate_entry_hour(self, value):
        if value < Registration.MIN_ENTRY_DATE or value > Registration.MAX_ENTRY_DATE:
            raise serializers.ValidationError('Entry hour is out of range')
        return value
    def validate_exit_hour(self, value):
        if value < Registration.MIN_ENTRY_DATE or value > Registration.MAX_ENTRY_DATE:
            raise serializers.ValidationError('Entry hour is out of range')
        return value

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
            'entry_hour',
            'exit_hour',
        )


