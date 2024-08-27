from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.relations import SlugRelatedField

from applications.sakura.models import Question, CaptureCard


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "serial_number",
            "question",
            "theme",
        )


class CaptureCardSerializer(serializers.ModelSerializer):
    attendee = HiddenField(default=CurrentUserDefault())
    card = SlugRelatedField(slug_field="slug", queryset=Question.objects.all())
    answer = serializers.CharField(write_only=True)

    def validate(self, attrs):
        card = attrs.get('card')
        answer = attrs.pop('answer')
        if not card.evaluate_question(answer):
            raise serializers.ValidationError("Respuesta incorrecta")
        return attrs

    class Meta:
        model = CaptureCard
        fields = (
            'attendee',
            'card',
            'answer'
        )