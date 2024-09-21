from rest_framework import viewsets, mixins

from applications.instagram.models import Photo
from applications.instagram.serializers import PhotoSerializer


class PhotoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Photo.objects.all().order_by('created_at')
    serializer_class = PhotoSerializer