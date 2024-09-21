from django.contrib import admin
from django.utils.html import format_html

from applications.instagram.models import Photo


# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    def picture(self, obj):
        return format_html('<img src="{}" width=50 />'.format(obj.image.url)) if obj.image else None

    list_display = ('image', 'description', 'picture')

    ordering = ('-created_at',)

admin.site.register(Photo, PhotoAdmin)