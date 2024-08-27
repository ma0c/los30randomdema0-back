import re

from django.db import models

from los30randomdema0.base_model import BaseModel

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
