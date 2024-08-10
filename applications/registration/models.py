from django.db import models

from los30randomdema0.base_model import BaseModel
from django.utils.crypto import get_random_string

# Create your models here.

class PossibleAttendees(BaseModel):
    """
    This model represents the possible attendees to the event
    """

    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    instagram = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='attendees/', null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', 'phone'], name='unique_name_phone_index')
        ]
        constraints = [
            models.UniqueConstraint(fields=['name', 'phone'], name='unique_name_phone_constraint')
        ]


class Registration(BaseModel):
    """
    This model represents the concrete registration to the event
    """
    possible_attendee = models.OneToOneField(PossibleAttendees, related_name="registered_attendee", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    extra_attendees = models.IntegerField()
    vegetarian = models.CharField(max_length=1, default='N')
    alcohol = models.CharField(max_length=1, blank=True)
    weed = models.CharField(max_length=1)
    is_confirmed = models.BooleanField(default=False)


class AttendeeToken(BaseModel):
    token = models.CharField(max_length=100)
    attendee = models.ForeignKey(PossibleAttendees, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)