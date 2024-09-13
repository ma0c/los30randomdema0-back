import re

from django.db import models

from los30randomdema0.base_model import BaseModel
from applications.registration.models import PossibleAttendees

EXACT = 'exacta'
TERMS = 'terminos'


def tokenize(text: str) -> set:
    return set(re.split(r'\W+|,|-', sanitize(text)))

def sanitize(text: str) -> str:
    return text.strip().lower().replace(
        'á', 'a'
    ).replace(
        'é', 'e'
    ).replace(
        'í', 'i'
    ).replace(
        'ó', 'o'
    ).replace(
        'ú', 'u'
    )

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default="#000000")
    image = models.ImageField(upload_to='card-categories/', null=True, blank=True)
    front_image = models.ImageField(upload_to='card-categories-front/', null=True, blank=True)
    is_special = models.BooleanField(default=False)
    question_in_category = models.IntegerField(default=5)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['slug'], name='unique_category_slug'),
        ]

    def __str__(self):
        return self.name

class Question(BaseModel):

    serial_number = models.IntegerField(unique=True)
    question = models.TextField()
    answer = models.TextField()
    theme = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="questions", on_delete=models.CASCADE, null=True)
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
        print(f"Evaluating {answer} against {self.answer} using {self.evaluation_type}")
        evaluation_split = self.evaluation_type.split()
        evaluation_type = evaluation_split[0].lower()
        if evaluation_type == EXACT:
            print(sanitize(answer) == sanitize(self.answer))
            return sanitize(answer) == sanitize(self.answer)
        elif evaluation_type == TERMS:
            expected_answer = tokenize(self.answer)
            user_answer = tokenize(answer)
            expected_count, total_count = evaluation_split[1].split('/')
            expected_count = int(expected_count)
            total_count = int(total_count)
            print(f"{len(expected_answer.intersection(user_answer))} >= {expected_count}")
            print(len(expected_answer.intersection(user_answer)) >= expected_count)
            return len(expected_answer.intersection(user_answer)) >= expected_count


class CaptureCard(BaseModel):
    attendee = models.ForeignKey(PossibleAttendees, related_name="captured_cards", on_delete=models.CASCADE)
    card = models.ForeignKey(Question, related_name="captured_by", on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)

    class Meta:
        ordering = ['attendee', 'card__serial_number']
        constraints = [
            models.UniqueConstraint(fields=['attendee', 'card'], name='unique_capture_card_attendee_card'),
        ]

    def __str__(self):
        return f"{self.attendee} captured {self.card}"

class CardAttempt(BaseModel):
    card = models.ForeignKey(Question, related_name="attempts", on_delete=models.CASCADE)
    attendee = models.ForeignKey(PossibleAttendees, related_name="attempts", on_delete=models.CASCADE)
    answer = models.TextField()
    solved = models.BooleanField(default=False)

    class Meta:
        ordering = ['attendee', 'card__serial_number']


    def __str__(self):
        return f"{self.attendee} attempted {self.card}"