import qrcode
from django.contrib import admin
from django.utils.html import format_html
from qrcode.image.svg import SvgPathImage

from applications.sakura.models import Question


class CardModelAdmin(admin.ModelAdmin):
    def qr_code(self, obj):
        img = qrcode.make(obj.slug, image_factory=SvgPathImage)
        img_string = img.to_string(encoding='unicode')
        return format_html(img_string)

    qr_code.short_description = 'QR Code'

    list_display = ('serial_number', 'theme', 'slug', 'qr_code')


admin.site.register(Question, CardModelAdmin)

