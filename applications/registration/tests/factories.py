from factory.django import DjangoModelFactory
from factory import SubFactory
from applications.registration.models import PossibleAttendees, Registration


class PossibleAttendeesFactory(DjangoModelFactory):
    class Meta:
        model = PossibleAttendees

    name = 'ma0'
    phone = '1234567890'


class RegistrationFactory(DjangoModelFactory):
    class Meta:
        model = Registration

    possible_attendee = SubFactory(PossibleAttendeesFactory)
    name = 'ma0'
    phone = '1234567890'
    whatsapp_number = '1234567890'
    extra_attendees = 0
    alcohol = 'N'
    weed = 'N'
    is_confirmed = True