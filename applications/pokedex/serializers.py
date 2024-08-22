from rest_framework.serializers import ModelSerializer
from applications.pokedex.models import Badge, Profile, Connection
from applications.registration import serializers as registration_serializers


class BadgeSerializer(ModelSerializer):
    class Meta:
        model = Badge
        fields = (
            "name",
            "image"
        )

class ProfileSerializer(ModelSerializer):
    attendee = registration_serializers.PossibleAttendeesSerializer()
    badges = BadgeSerializer(many=True)
    class Meta:
        model = Profile
        fields = (
            "attendee",
            "badges",
            "number"
        )


class PokedexSerializer(ModelSerializer):
    attendee = registration_serializers.PossibleAttendeesSerializer()

    class Meta:
        model = Profile
        fields = (
            "attendee",
            "number"
        )


class ConnectionSerializer(ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"