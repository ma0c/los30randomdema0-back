from applications.registration import authentication as registration_mixin

class IsAuthenticatedAppMixin:
    authentication_classes = [registration_mixin.TokenAuthentication]
    permission_classes = [registration_mixin.IsAuthenticated]