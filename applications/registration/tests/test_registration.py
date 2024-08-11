from copy import deepcopy
from uuid import uuid4
from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ErrorDetail
from applications.registration.tests.factories import PossibleAttendeesFactory, RegistrationFactory
from applications.registration.viewsets import RegistrationViewSet, PossibleAttendeesViewSet


class TestRegistration(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.possible_attendee = PossibleAttendeesFactory()
        self.complete_payload = {
            "possible_attendee": self.possible_attendee.id,
            "name": "ma0",
            "phone": "1234567890",
            "whatsapp_number": "1234567890",
            "extra_attendees": 0,
            "alcohol": "N",
            "weed": "N"
        }

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

    def test_get_registered_attendee_in_possible_attendee_payload(self):
        payload = deepcopy(self.complete_payload)
        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201
        registration_id = response.data['id']

    def test_retrieve_already_registered_attendee(self):
        RegistrationFactory(possible_attendee=self.possible_attendee)
        request = self.factory.get(f'/registration/{self.possible_attendee.slug}')
        response = PossibleAttendeesViewSet.as_view({'get': 'retrieve'})(request, slug=self.possible_attendee.slug)
        assert response.status_code == 400
        assert response.data['detail'] == 'Possible Attendee already exist, update the existing one instead of creating a new one.'

    def test_retrieve_non_registered_attendee(self):
        request = self.factory.get(f'/registration/{self.possible_attendee.slug}')
        response = PossibleAttendeesViewSet.as_view({'get': 'retrieve'})(request, slug=self.possible_attendee.slug)
        assert response.status_code == 200
        assert response.data['name'] == self.possible_attendee.name
        assert response.data['phone'] == self.possible_attendee.phone
        assert response.data['instagram'] == self.possible_attendee.instagram
        assert response.data['profile_pic'] == self.possible_attendee.profile_pic
        assert response.data['registered_attendee'] is None

    def test_invalid_entry_time(self):
        payload = deepcopy(self.complete_payload)
        payload['entry_hour'] = '2024-09-14T15:59'
        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 400
        assert response.data['entry_hour'][0] == 'Entry hour is out of range'

    def test_valid_entry_exit_times(self):
        payload = deepcopy(self.complete_payload)
        payload['entry_hour'] = '2024-09-14T16:00'
        payload['exit_hour'] = '2024-09-15T17:00'
        request = self.factory.post('/registration/', payload, format='json')
        response = RegistrationViewSet.as_view({'post': 'create'})(request)
        assert response.status_code == 201
        assert payload['entry_hour'] in response.data['entry_hour']
        assert payload['exit_hour'] in response.data['exit_hour']
