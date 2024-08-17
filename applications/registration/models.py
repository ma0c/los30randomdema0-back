from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import models

from los30randomdema0.base_model import BaseModel
from django.utils.crypto import get_random_string


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

    def __repr__(self):
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

    MIN_ENTRY_DATE = datetime(year=2024, month=9, day=14, hour=16, minute=0, tzinfo=ZoneInfo(key='UTC'))
    MAX_ENTRY_DATE = datetime(year=2024, month=9, day=15, hour=22, minute=0, tzinfo=ZoneInfo(key='UTC'))

    possible_attendee = models.OneToOneField(PossibleAttendees, related_name="registered_attendee", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    extra_attendees = models.IntegerField()
    vegetarian = models.CharField(max_length=1, default='N')
    alcohol = models.CharField(max_length=1, blank=True)
    weed = models.CharField(max_length=1)
    entry_hour = models.DateTimeField(null=True, blank=True)
    exit_hour = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=True)
    slug = models.SlugField(max_length=500, unique=True, null=True)
    instagram = models.CharField(max_length=100, blank=True)


class AttendeeToken(BaseModel):
    token = models.CharField(max_length=100)
    attendee = models.ForeignKey(PossibleAttendees, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)