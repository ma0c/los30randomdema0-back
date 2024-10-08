from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from applications.pokedex.models import Badge, Profile, Connection


class ProfileAdmin(admin.ModelAdmin):
    def badge_list(self, obj):
        return format_html("-".join(
            [
                f"<img src='{badge.image.url if badge.image else None}' alt='{badge.name}' width=30 />"
                for badge in obj.badges.all()
            ]
        )
        )

    def image_tag(self, obj):
        return format_html('<img src="{}" width=50 />'.format(obj.attendee.profile_pic.url)) if obj.attendee.profile_pic else None


    list_display = ('number', 'attendee', 'image_tag', 'badge_list', 'is_enabled')
    search_fields = ('attendee__name',)

class BadgeAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width=50 />'.format(obj.image.url)) if obj.image else None
    list_display = ('name', 'image_tag')
    search_fields = ('name',)


admin.site.register(Badge, BadgeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Connection)
