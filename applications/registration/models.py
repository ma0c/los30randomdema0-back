from django.db import models

from los30randomdema0.base_model import BaseModel


# Create your models here.

class PossibleAttendees(BaseModel):
    """
    This model represents the possible attendees to the event
    """
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)


class Registration(BaseModel):
    """
    This model represents the concrete registration to the event
    """
    possible_attendee = models.ForeignKey(PossibleAttendees, on_delete=models.CASCADE, null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)