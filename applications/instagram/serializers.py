from rest_framework import serializers

from applications.instagram.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image', 'description', 'created_at']
        ordering = ('-created_at',)