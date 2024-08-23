from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, HiddenField, ValidationError

from applications.pokedex.fields import CurrentProfileDefault
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


class CreateConnectionSerializer(ModelSerializer):
    follower = HiddenField(default=CurrentProfileDefault())
    followed = SlugRelatedField(slug_field="attendee__slug", queryset=Profile.objects.all())

    def validate_followed(self, value):
        if value == self.context['request'].user.profile:
            raise ValidationError("You cannot follow yourself.")
        return value
    class Meta:
        model = Connection
        fields = (
            'followed',
            'follower'
        )