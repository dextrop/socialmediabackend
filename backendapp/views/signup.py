from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from backendapp.controllers.usercontroller import UserController
from backendapp.lib.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser

class SignupView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        controller = UserController()
        result = controller.signup(request.data.dict())
        if not result['status']:
            return CustomResponse(message=result['message'], code=status.HTTP_400_BAD_REQUEST)

        return CustomResponse(message=result['message'], code=status.HTTP_201_CREATED)

