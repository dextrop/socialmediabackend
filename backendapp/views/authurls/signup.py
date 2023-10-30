from rest_framework import generics, status
from backendapp.middlewares.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser
from backendapp.serializers.userserializer import UsersSerializer, Users

class SignupView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            # print (request.Files)
            serializer = UsersSerializer(data=request.data)
            if serializer.is_valid():
                user_data = serializer.validated_data
                Users.objects.create_user(**user_data)
                return CustomResponse(code=status.HTTP_201_CREATED, message= 'User created successfully')
            else:
                return CustomResponse(code=status.HTTP_400_BAD_REQUEST, message=serializer.errors)
        except Exception as e:
            print (e)
            return CustomResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

