from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.relations import SlugRelatedField

from applications.sakura.models import Question, CaptureCard, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "color",
            "image",
            "front_image",
            "is_special",
            "question_in_category"
        )

class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Question
        fields = (
            "serial_number",
            "slug",
            "question",
            "theme",
            "category"
        )


class CapturedCardSerializer(serializers.ModelSerializer):
    card = QuestionSerializer()
    class Meta:
        model = CaptureCard
        fields = (
            "card",
            "solved"
        )


class CaptureCardSerializer(serializers.ModelSerializer):
    attendee = HiddenField(default=CurrentUserDefault())
    card = SlugRelatedField(slug_field="slug", queryset=Question.objects.all())
    answer = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if self.instance and self.instance.solved:
            raise serializers.ValidationError("Card already solved")

        card = attrs.get('card', self.instance.card if self.instance else None)
        answer = attrs.pop('answer')
        if card is None:
            raise serializers.ValidationError("Card not provided")
        attrs["solved"] = card.evaluate_question(answer)
        return attrs

    class Meta:
        model = CaptureCard
        fields = (
            'attendee',
            'card',
            'answer',
            'solved'
        )