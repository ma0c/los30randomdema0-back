import re

from django.db import models

from los30randomdema0.base_model import BaseModel
from applications.registration.models import PossibleAttendees

EXACT = 'exacta'
TERMS = 'terminos'


def tokenize(text: str) -> set:
    return set(re.split(r'\W+|,|-', text.lower()))


class Question(BaseModel):

    serial_number = models.IntegerField(unique=True)
    question = models.TextField()
    answer = models.TextField()
    theme = models.CharField(max_length=255)
    responsible = models.CharField(max_length=255)
    evaluation_type = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['serial_number']
        constraints = [
            models.UniqueConstraint(fields=['serial_number'], name='unique_question_serial_number'),
            models.UniqueConstraint(fields=['slug'], name='unique_question_slug'),
        ]

    def __str__(self):
        return f"{self.serial_number}-{self.theme}"

    def evaluate_question(self, answer: str) -> bool:
        evaluation_split = self.evaluation_type.split()
        evaluation_type = evaluation_split[0].lower()
        if evaluation_type == EXACT:
            return answer.strip().lower() == self.answer.lower()
        elif evaluation_type == TERMS:
            expected_answer = tokenize(self.answer)
            user_answer = tokenize(answer)
            expected_count, total_count = evaluation_split[1].split('/')
            expected_count = int(expected_count)
            total_count = int(total_count)
            return len(expected_answer.intersection(user_answer)) >= expected_count


class CaptureCard(BaseModel):
    attendee = models.ForeignKey(PossibleAttendees, related_name="captured_cards", on_delete=models.CASCADE)
    card = models.ForeignKey(Question, related_name="captured_by", on_delete=models.CASCADE)

    class Meta:
        ordering = ['attendee', 'card__serial_number']
        constraints = [
            models.UniqueConstraint(fields=['attendee', 'card'], name='unique_capture_card_attendee_card'),
        ]

    def __str__(self):
        return f"{self.attendee} captured {self.card}"
