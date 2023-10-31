from django.urls import reverse
from urllib.parse import urlencode
import base64, hashlib, random, string, os
from oauth2_provider.models import Application
from django.conf import settings

class OAuthController():
    def get_application(self):
        """
        The project is a prototype/exercise so assuming only one application
        will be used for OAuth, if more than 1 application is intended to be use,
        use Application ID to create OAuth Application Model
        """
        return Application.objects.first()

    def get_client_secret(self):
        return settings.APP_CONF["OAUTH_CLIENT_SECRET"]

    def generate_oauth_url(self):
        """Generate OAuth authorize url for provided code challenge."""
        application = self.get_application()
        code_verifier = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

        base_url = settings.APP_CONF["BASE_URI"] + reverse('oauth2_provider:authorize')
        data = {
            "client_id": settings.APP_CONF["OAUTH_CLIENT_ID"],
            "response_type": "code",
            "redirect_uri": settings.APP_CONF["OAUTH_CLIENT_URIS"],
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": code_verifier
        }
        query_params = urlencode(data)
        return f"{base_url}?{query_params}"

    def generate_token_url(self, code, code_verifier):
        """Generate OAuth Token"""
        data = {
            "client_id": settings.APP_CONF["OAUTH_CLIENT_ID"],
            "client_secret": settings.APP_CONF["OAUTH_CLIENT_SECRET"],
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": settings.APP_CONF["OAUTH_CLIENT_URIS"],
            "grant_type": "authorization_code",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache"}
        url = settings.APP_CONF["BASE_URI"] + reverse('oauth2_provider:token')
        return {"url": url, "data": data, "headers":headers }