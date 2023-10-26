import requests
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
        data = {
            "client_id": application.client_id,
            "client_secret": "6wNOJdZa4X8qq4wRX0HojHCInJgfyS6ch9DpJegRy3oMOlAfoszXpsVe2U75AbPjoEDQtNoV16rz2lwbgb9jdqhUlb53EQaJSEsAL0DzibLVLFmqOgzXHZoCwOQLFscm",
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": application.redirect_uris,
            "grant_type": "authorization_code",
        }
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded","Cache-Control": "no-cache"}
            resp = requests.post("http://localhost:8000/oauth/token/", data=data, headers=headers)
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)