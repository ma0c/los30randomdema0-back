from django.urls import path

from applications.analytics import views

urlpatterns = [
    path('registration-report/', views.RegistrationReport.as_view(), name='registration-report'),
]