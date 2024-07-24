from copy import deepcopy
from uuid import uuid4
from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ErrorDetail
from applications.registration.tests.factories import PossibleAttendeesFactory
from applications.registration.viewsets import RegistrationViewSet, PossibleAttendeesViewSet


class TestRegistration(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        possible_attendee = PossibleAttendeesFactory()
        self.complete_payload = {
            "possible_attendee": possible_attendee.id,
            "name": "ma0",
            "phone": "1234567890",
            "whatsapp_number": "1234567890",
            "extra_attendees": 0,
            "alcohol": "N",
            "weed": "N"
        }


    def test_possiblee_attendees_list(self):
        request = self.factory.get('/possible_attendees/')
        possible_attendee = PossibleAttendeesFactory()
        response = PossibleAttendeesViewSet.as_view({'get': 'list'})(request)
        assert response.status_code == 200
        assert response.data[0]['name'] == possible_attendee.name
        assert response.data[0]['phone'] == possible_attendee.phone

    def test_registration_post_complete_payload(self):
        payload = deepcopy(self.complete_payload)

        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201
        assert response.data['name'] == payload['name']
        assert response.data['phone'] == payload['phone']
        assert response.data['whatsapp_number'] == payload['whatsapp_number']
        assert response.data['extra_attendees'] == payload['extra_attendees']
        assert response.data['alcohol'] == payload['alcohol']
        assert response.data['weed'] == payload['weed']

    def test_registration_with_no_registered_attendee(self):
        payload = deepcopy(self.complete_payload)
        non_existing_attendee_id = uuid4()
        payload['possible_attendee'] = non_existing_attendee_id
        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 400
        assert response.data['possible_attendee'][0] == f'Invalid pk "{non_existing_attendee_id}" - object does not exist.'

    def test_registrate_already_registered_attendee(self):
        payload = deepcopy(self.complete_payload)
        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201

        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 400
        assert response.data['error'] == 'Possible Attendee already exist, update the existing one instead of creating a new one.'

    def test_update_registered_attendee(self):
        payload = deepcopy(self.complete_payload)
        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201

        payload['whatsapp_number'] = '1234567891'
        request = self.factory.put(f'/registration/{response.data["id"]}/', payload, format='json')
        response = RegistrationViewSet.as_view({'put': 'update'})(request, pk=response.data['id'])
        assert response.status_code == 200
        assert response.data['whatsapp_number'] == payload['whatsapp_number']
