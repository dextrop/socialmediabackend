from rest_framework import generics, status
from backendapp.lib.custom_response import CustomResponse
from rest_framework.permissions import IsAuthenticated
from backendapp.serializers.userserializer import UsersSerializer

class UserView(generics.GenericAPIView):
    allowed_methods = ("GET", "PUT", )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return CustomResponse(
            message="Test API", code=status.HTTP_201_CREATED, payload=UsersSerializer(request.user).data
        )

