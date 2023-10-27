import os

import requests
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from oauth2_provider.models import Application

class AuthCallbackView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("GET",)

    def get(self, request):
        code = request.GET.get('code')
        code_verifier = request.GET.get('state')
        application = Application.objects.first()
        client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
        print ("Client Secret", client_secret)
        data = {
            "client_id": application.client_id,
            "client_secret": client_secret,
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": application.redirect_uris,
            "grant_type": "authorization_code",
        }
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded","Cache-Control": "no-cache"}
            url = os.environ.get("BASE_URL") + reverse('oauth2_provider:token')
            resp = requests.post(url, data=data, headers=headers)
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print (e)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)