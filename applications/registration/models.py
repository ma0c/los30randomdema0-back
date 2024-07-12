from django.db import models


# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    extra_attendees = models.IntegerField()
    alcohol = models.CharField(max_length=1)
    weed = models.CharField(max_length=1)


class PossibleAttendees(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    already_registered = models.BooleanField(default=False)
