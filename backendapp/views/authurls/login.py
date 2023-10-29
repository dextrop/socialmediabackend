from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from backendapp.controllers.authcontroller import OAuthController

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("POST",)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            oauth_url = OAuthController().generate_oauth_url()
            return Response(
                {
                    "payload": oauth_url,
                    "message":"Authentication Successful, continue with authorization.",
                    "code":status.HTTP_200_OK
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)