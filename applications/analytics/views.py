from faulthandler import is_enabled

import qrcode
import urllib.parse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.generic import ListView, DetailView, TemplateView
from qrcode.image.svg import SvgPathImage

from applications.registration.models import Registration, PossibleAttendees, AttendeeToken
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
        token, created = AttendeeToken.objects.get_or_create(attendee=self.object)
        if created:
            token.generate_token()

        context['app_url'] = urllib.parse.quote_plus(f'https://app.los30randomdema0.com/token/{token.token}')
        return context

class Leaderboard(TemplateView):
    template_name = 'analytics/leaderboard.html'
    context_object_name = 'leaderboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        connections = Profile.objects.filter(
            ~Q(possibleattendees__name='Ma0'),
            is_enabled=True,
            is_active=True,
        ).annotate(connections=Count('following')).filter(connections__gt=0).order_by('-connections')
        context['connections'] = connections
        cards = PossibleAttendees.objects.filter(
            ~Q(name='Ma0')
        ).annotate(
            cards=Count('captured_cards')
        ).filter(
            cards__gt=0
        ).order_by('-cards')
        context['cards'] = cards
        return context