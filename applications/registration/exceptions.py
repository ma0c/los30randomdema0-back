from rest_framework.exceptions import APIException
from rest_framework import status


class AttendeeAlreadyRegisteredException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": 'Possible Attendee already exist, update the existing one instead of creating a new one.'
    }
    default_code = 1

    def __init__(self, registration):
        self.default_detail["redirect"] = registration.slug
        super().__init__(self.default_detail)
        self.registration = registration
