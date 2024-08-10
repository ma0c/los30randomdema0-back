from rest_framework.exceptions import APIException
from rest_framework import status


class AttendeeAlreadyRegisteredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Possible Attendee already exist, update the existing one instead of creating a new one.'
    default_code = 1

    def __init__(self, registration):
        super().__init__(self.default_detail)
        self.registration = registration
