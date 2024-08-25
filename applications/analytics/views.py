import qrcode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import ListView, DetailView
from qrcode.image.svg import SvgPathImage

from applications.registration.models import Registration, PossibleAttendees
from applications.pokedex.models import Badge, Profile, Connection


# Create your views here.


@method_decorator(login_required, name='dispatch')
class RegistrationReport(ListView):
    template_name = 'analytics/registration_report.html'
    context_object_name = 'registrations'
    queryset = Registration.objects.all()


class PossibleAttendeesList(ListView):
    template_name = 'analytics/possible_attendees.html'
    context_object_name = 'possible_attendees'
    queryset = PossibleAttendees.objects.all()


class AttendeeProfile(DetailView):
    template_name = 'analytics/attendee_profile.html'
    context_object_name = 'attendee'
    queryset = PossibleAttendees.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration'] = Registration.objects.filter(possible_attendee=self.object).first()
        class CustomSvgPathImage(SvgPathImage):
            QR_PATH_STYLE = {
                "fill": "#ebecf0",
                "fill-opacity": "1",
                "fill-rule": "nonzero",
                "stroke": "none",
            }

        img = qrcode.make(self.object.slug, image_factory=CustomSvgPathImage, box_size=20)
        img_string = img.to_string(encoding='unicode')
        context['qr'] = format_html(img_string)
        context['profile'] = self.object.profile
        context['followers'] = Connection.objects.filter(followed=self.object.profile)
        context['following'] = Connection.objects.filter(follower=self.object.profile)
        context['total_active_profiles'] = Profile.objects.filter(
            # is_active=True,
            is_enabled=True
        ).count()
        return context
