from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from applications.registration.models import Registration
# Create your views here.


@method_decorator(login_required, name='dispatch')
class RegistrationReport(ListView):
    template_name = 'analytics/registration_report.html'
    context_object_name = 'registrations'
    queryset = Registration.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registrations'] = self.get_queryset()
        return context