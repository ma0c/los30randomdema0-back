from django.db import models


# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    extra_attendees = models.IntegerField()
    vegetarian = models.CharField(max_length=1, default='N')
    alcohol = models.CharField(max_length=1)
    weed = models.CharField(max_length=1)


class PossibleAttendees(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    registered_attendee = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True)


class AttendeeToken(models.Model):
    token = models.CharField(max_length=100)
    attendee = models.ForeignKey(PossibleAttendees, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)