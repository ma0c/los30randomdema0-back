from factory.django import DjangoModelFactory

from applications.registration.models import PossibleAttendees


class PossibleAttendeesFactory(DjangoModelFactory):
    class Meta:
        model = PossibleAttendees

    name = 'ma0'
    phone = '1234567890'