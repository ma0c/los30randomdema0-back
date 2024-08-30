from rest_framework import viewsets, mixins

from applications.registration.mixins import IsAuthenticatedAppMixin
from applications.sakura.models import CaptureCard, Question
from applications.sakura.serializers import CapturedCardSerializer, CaptureCardSerializer, QuestionSerializer


class CardViewSet(
    IsAuthenticatedAppMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin
):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'


class CapturedCardsViewSet(
    IsAuthenticatedAppMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    serializer_class = CapturedCardSerializer

    def get_queryset(self):
        return CaptureCard.objects.filter(attendee=self.request.user)


class CaptureCardViewSet(
    IsAuthenticatedAppMixin
    , viewsets.GenericViewSet
    , mixins.CreateModelMixin
    , mixins.UpdateModelMixin
):
    serializer_class = CaptureCardSerializer
    lookup_field = 'card__slug'

    def get_object(self):
        return CaptureCard.objects.get(
            attendee=self.request.user,
            card__slug=self.kwargs['card__slug']
        )

