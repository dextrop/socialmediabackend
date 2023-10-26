from backendapp.serializers.userserializer import UsersSerializer
from backendapp.models.users import Users

class UserController():
    def __init__(self):
        print ("User Controller")

    def signup(self, req_data):
        serializer = UsersSerializer(data=req_data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            Users.objects.create_user(**user_data)
            return {'status': True, 'message': 'User created successfully'}
        else:
            return {'status': False, 'message': serializer.errors}
