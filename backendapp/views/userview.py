from rest_framework import generics, status
from backendapp.middlewares.custom_response import CustomResponse
from rest_framework.permissions import IsAuthenticated

from backendapp.middlewares.logginmixin import LoggingMixin
from backendapp.serializers.userserializer import UsersSerializer

class UserView(generics.GenericAPIView, LoggingMixin):
    allowed_methods = ("GET", "PUT", )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        Returns the serialized user data. The response includes
        The response includes a message, a status code, and serialized user data as payload
        """
        return CustomResponse(
            message="Test API",
            code=status.HTTP_201_CREATED,
            payload=UsersSerializer(request.user).data
        )

