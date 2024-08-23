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

    class AlcoholChoices(models.TextChoices):
        NO = '1', 'Voy Manejando'
        A_LITTLE = '2', 'Un par de copitas y melo'
        A_LOT = '3', 'Si gotea repito'
        YESSS = '4', 'Voy a hacer una elmada, traigame un balde'

    class VegetarianChoices(models.TextChoices):
        VEGETARIAN = '1', 'Vegetariano'
        TOTALITARIAN = '2', 'Me como lo que me pongan'
        KOSHER = '3', 'Soy judio'
        OBNOXIOUS = '4', 'Soy vegano, fastidioso y voy a llevar mi propia comida'


    class WeedChoices(models.TextChoices):
        NO = '1', 'Nada, mi mama no me deja'
        A_LITTLE = '2', 'Par de ploncitos'
        YES = '3', 'Si sobra me llevo'
        IM_A_STONER = '4', 'Llevo quien me pilotee que voy al infinito y mas alla'

    possible_attendee = models.OneToOneField(PossibleAttendees, related_name="registered_attendee", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    extra_attendees = models.IntegerField()
    vegetarian = models.CharField(max_length=1, default='N', choices=VegetarianChoices.choices)
    alcohol = models.CharField(max_length=1, blank=True, choices=AlcoholChoices.choices)
    weed = models.CharField(max_length=1, choices=WeedChoices.choices)
    entry_hour = models.DateTimeField(null=True, blank=True)
    exit_hour = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=True)
    slug = models.SlugField(max_length=500, unique=True, null=True)
    instagram = models.CharField(max_length=100, blank=True)


class AttendeeToken(BaseModel):
    token = models.CharField(max_length=100)
    attendee = models.ForeignKey(PossibleAttendees, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attendee} - {self.token}"