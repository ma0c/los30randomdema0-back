from django.test import TestCase

from rest_framework.test import APIRequestFactory

from applications.registration.tests.factories import PossibleAttendeesFactory
from applications.registration.viewsets import RegistrationViewSet


class TestRegistration(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_registration_post_complete_payload(self):
        possible_attendee = PossibleAttendeesFactory()
        complete_payload = {
            "possible_attendee": possible_attendee.id,
            "name": "ma0",
            "phone": "1234567890",
            "whatsapp_number": "1234567890",
            "extra_attendees": 0,
            "alcohol": "N",
            "weed": "N"
        }
        request = self.factory.post('/registration/', complete_payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201
