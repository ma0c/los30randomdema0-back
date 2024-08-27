from rest_framework import viewsets, mixins

from applications.registration.mixins import IsAuthenticatedAppMixin
from applications.sakura.models import CaptureCard, Question
from applications.sakura.serializers import QuestionSerializer, CaptureCardSerializer


class CapturedCardsViewSet(
    IsAuthenticatedAppMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(captured_by__attendee=self.request.user)


class CaptureCardViewSet(
    IsAuthenticatedAppMixin
    , viewsets.GenericViewSet
    , mixins.CreateModelMixin
):
    serializer_class = CaptureCardSerializer
