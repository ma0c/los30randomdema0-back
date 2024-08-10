from django.contrib import admin
from django.utils.html import format_html

from applications.registration.models import PossibleAttendees, Registration


# Register your models here.


class PossibleAttendeesAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width=50 />'.format(obj.profile_pic.url)) if obj.profile_pic else None

    image_tag.short_description = 'Image'

    list_display = ('name', 'phone', 'slug', 'image_tag')
    search_fields = ('name', 'phone')


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'possible_attendee', 'name', 'phone', 'whatsapp_number', 'extra_attendees', 'vegetarian', 'alcohol', 'weed', 'is_confirmed')
    search_fields = ('name', 'phone')

admin.site.register(PossibleAttendees, PossibleAttendeesAdmin)
admin.site.register(Registration, RegistrationAdmin)
