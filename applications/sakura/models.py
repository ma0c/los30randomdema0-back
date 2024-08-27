from django.db import models

from los30randomdema0.base_model import BaseModel


# Create your models here.
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
