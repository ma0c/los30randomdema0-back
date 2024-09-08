import qrcode
from django.contrib import admin
from django.utils.html import format_html
from qrcode.image.svg import SvgPathImage

from applications.sakura.models import Question, CaptureCard, Category


class CategoryModelAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width: 200px; max-height:200px;">')
    def thumbnail_front(self, obj):
        return format_html(f'<img src="{obj.front_image.url if obj.front_image else None}" style="max-width: 200px; max-height:200px;">')

    thumbnail.short_description = 'Image'
    thumbnail_front.short_description = 'Image'

    list_display = ('name', 'thumbnail', 'thumbnail_front', 'is_special', 'question_in_category')




class CardModelAdmin(admin.ModelAdmin):
    def qr_code(self, obj):
        img = qrcode.make(obj.slug, image_factory=SvgPathImage)
        img_string = img.to_string(encoding='unicode')
        return format_html(img_string)

    qr_code.short_description = 'QR Code'

    list_display = ('serial_number', 'theme', 'slug', 'qr_code')


admin.site.register(Question, CardModelAdmin)
admin.site.register(CaptureCard)
admin.site.register(Category, CategoryModelAdmin)
