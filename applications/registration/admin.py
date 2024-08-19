from django.contrib import admin
from django.utils.html import format_html

from applications.registration.models import PossibleAttendees, Registration
import qrcode
from qrcode.image.svg import SvgPathImage


# Register your models here.


class PossibleAttendeesAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width=50 />'.format(obj.profile_pic.url)) if obj.profile_pic else None

    def qr_code(self, obj):
        img = qrcode.make(obj.slug, image_factory=SvgPathImage)
        img_string = img.to_string(encoding='unicode')
        return format_html(img_string)

    image_tag.short_description = 'Image'
    qr_code.short_description = 'QR Code'



    list_display = ('name', 'phone', 'slug', 'image_tag', 'qr_code')
    search_fields = ('name', 'phone')


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('slug', 'possible_attendee', 'name', 'phone', 'whatsapp_number', 'extra_attendees', 'vegetarian', 'alcohol', 'weed', 'is_confirmed')
    search_fields = ('name', 'phone')

admin.site.register(PossibleAttendees, PossibleAttendeesAdmin)
admin.site.register(Registration, RegistrationAdmin)
