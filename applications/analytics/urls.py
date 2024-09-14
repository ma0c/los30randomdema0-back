from django.urls import path

from applications.analytics import views

urlpatterns = [
    path('registration-report/', views.RegistrationReport.as_view(), name='registration-report'),
    path('attendee-list/', views.PossibleAttendeesList.as_view(), name='attendees-list'),
    path('attendee/<slug:slug>', views.AttendeeProfile.as_view(), name='attendee-profile'),
    path('leaderboard', views.Leaderboard.as_view(), name='leaderboard'),
]