from applications.pokedex.models import Profile
# from applications.registration.models import PossibleAttendees


class GetProfileFromAuthenticationMixin:
    def get_profile(self):
        # if not hasattr(self, 'request'):
        #     return None
        # if not hasattr(self.request, 'user'):
        #     return None
        # if not isinstance(self.request.user, PossibleAttendees):
        #     raise ValueError('User is not a PossibleAttendees')
        return Profile.objects.get(attendee=self.request.user)