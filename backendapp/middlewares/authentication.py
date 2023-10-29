from django.core.exceptions import ValidationError
from oauth2_provider.models import AccessToken
from backendapp.models.users import Users
from rest_framework import authentication
from rest_framework import exceptions

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """Custom authentication for OAuth, Default OAuth
        Token Authentication tends to throw CSRF error sometimes"""
        _token = request.META.get("HTTP_AUTHORIZATION")
        try:
            token = AccessToken.objects.get(token=_token.split(" ")[1])
            user = Users.objects.get(username=token.user)
            if not user.is_active:
                raise ValidationError("User not verified, verify.py user to continue using API's")
            return (user, token)
        except Exception as e:
            pass
        return None

    def authenticate_header(self, request):
        return ['authentication']