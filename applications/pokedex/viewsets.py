
from django.db.models import Q
from django.db import connection
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from applications.pokedex import serializers, models, mixins as pokedex_mixins
from applications.registration import authentication as registration_mixin


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    pokedex_mixins.GetProfileFromAuthenticationMixin,
    viewsets.GenericViewSet
    ):
    authentication_classes = [registration_mixin.TokenAuthentication]
    permission_classes = [registration_mixin.IsAuthenticated]
    serializer_class = serializers.ProfileSerializer
    queryset = serializers.ProfileSerializer.Meta.model.objects.all()
    lookup_field = 'attendee__slug'


class PokedexViewSet(
    mixins.ListModelMixin,
    pokedex_mixins.GetProfileFromAuthenticationMixin,
    viewsets.GenericViewSet
):
    authentication_classes = [registration_mixin.TokenAuthentication]
    permission_classes = [registration_mixin.IsAuthenticated]
    serializer_class = serializers.PokedexSerializer
    me = None

    def get_queryset(self):
        """
        We'd like to run this query

        ```sql
WITH flattened_profiles AS (
    SELECT
        profile.id
        , attendee.name
        , attendee.profile_pic
    FROM pokedex_profile profile
    JOIN registration_possibleattendees attendee on profile.attendee_id = attendee.id
    WHERE NOT (
        profile.attendee_id = '9efd7aea-0987-4e57-a611-c75617ef4514'::uuid
    )
)
SELECT
    profile.id
    , profile.name
    , profile.profile_pic
    , connection.followed_id
    , connection.follower_id
FROM flattened_profiles profile
LEFT OUTER JOIN pokedex_connection connection ON  profile.id = connection.followed_id
WHERE connection.follower_id = '9a950263-d13d-417b-a3ed-0cf80c8e0abe' OR connection.follower_id IS NULL;
        ```
        But django ORM is not capable of doing this. So we'll have to do it in two steps.
        """
        queryset = models.Profile.objects.filter(
            ~Q(id=self.me.id)
        ).prefetch_related(
            "attendee",
            "badges",
            "followers"
        ).order_by("number")
        connections = models.Connection.objects.filter(
            follower_id=self.me.id
        ).values_list("followed_id", flat=True)
        print(connections)
        for profile in queryset:
            if profile.id not in connections:
                profile.attendee = None

        return queryset

    def list(self, request, *args, **kwargs):
        self.me = self.get_profile()
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ConnectionViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.ConnectionSerializer
    queryset = serializers.ConnectionSerializer.Meta.model.objects.all()
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
