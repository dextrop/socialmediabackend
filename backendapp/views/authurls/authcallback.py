import requests
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backendapp.controllers.authcontroller import OAuthController

class AuthCallbackView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("GET",)

    def get(self, request):
        code = request.GET.get('code')
        code_verifier = request.GET.get('state')
        oauthtokenresp = OAuthController().generate_token_url(code, code_verifier)
        try:
            resp = requests.post(
                oauthtokenresp["url"],
                data=oauthtokenresp["data"],
                headers=oauthtokenresp["headers"]
            )
            return Response(resp.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print (e)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)