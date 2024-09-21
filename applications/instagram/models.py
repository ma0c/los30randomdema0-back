from django.db import models

from los30randomdema0.base_model import BaseModel


# Create your models here.
class Photo(BaseModel):
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description