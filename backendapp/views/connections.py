from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from backendapp.lib.custom_response import CustomResponse
from backendapp.controllers.connections_controller import ConnectionsController

MSG = "Connection API's"
class ConnectionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def _setup(self, request, raise_username_exception=False):
        username = request.data.get("username", None)
        controller = ConnectionsController(request.user)
        if not username and raise_username_exception:
            raise ValidationError("Missing Username")
        return username, controller

    def get(self, request):
        username, controller = self._setup(request)
        resp = controller.get_all_connection(),
        return CustomResponse(message=MSG, payload=resp, code=status.HTTP_200_OK)

    def post(self, request):
        username, controller = self._setup(request, True)
        response = controller.add_connection(username)
        return CustomResponse(message=MSG, payload = response, code=status.HTTP_200_OK)

    def put(self, request):
        username, controller = self._setup(request, True)
        resp = controller.approve_connection(username)
        return CustomResponse(message=MSG, payload=resp, code=status.HTTP_200_OK)

    def delete(self, request):
        username, controller = self._setup(request, True)
        resp = controller.remove_connection(username)
        return CustomResponse(message=MSG, payload=resp, code=status.HTTP_200_OK)