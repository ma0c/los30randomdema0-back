from django.contrib import admin

from applications.registration.models import PossibleAttendees, Registration


# Register your models here.


class PossibleAttendeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    search_fields = ('name', 'phone')


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'possible_attendee', 'name', 'phone', 'whatsapp_number', 'extra_attendees', 'vegetarian', 'alcohol', 'weed', 'is_confirmed')
    search_fields = ('name', 'phone')

admin.site.register(PossibleAttendees, PossibleAttendeesAdmin)
admin.site.register(Registration, RegistrationAdmin)
