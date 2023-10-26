import json
from urllib.parse import urlencode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from oauth2_provider.models import Application
from django.contrib.auth import authenticate, login
from django.core.cache import cache
import random, string, base64, hashlib

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("POST",)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        application = Application.objects.first()
        if user is not None:
            login(request, user)

            code_verifier = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

            code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
            code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

            base_url = "http://localhost:8000/oauth/authorize/"
            data = {
                "client_id": application.client_id,
                "response_type": "code",
                "redirect_uri": application.redirect_uris,
                "code_challenge": code_challenge,
                "code_challenge_method":"S256",
                "state": code_verifier
            }
            query_params = urlencode(data)
            oauth_url = f"{base_url}?{query_params}"

            return Response({"authorization_url": oauth_url}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)