from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from backendapp.middlewares.custom_response import CustomResponse
from backendapp.controllers.connections_controller import ConnectionsController

MSG = "Connection API's"

class ConnectionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def _setup(self, request):
        """Initial View Setup, Include check for username
        and create a controller for connections"""
        username = request.data.get("username", None)
        controller = ConnectionsController(request.user)
        if not username:
            raise ValidationError("Missing Username")
        return username, controller

    def get(self, request):
        """Get All connections"""
        controller = ConnectionsController(request.user)
        resp = controller.get_all_connection(),
        return CustomResponse(message=MSG, payload=resp, code=status.HTTP_200_OK)

    def post(self, request):
        """Add new connection"""
        username, controller = self._setup(request)
        response = controller.add_connection(username)
        return CustomResponse(message=MSG, payload = response, code=status.HTTP_200_OK)

    def put(self, request):
        """Approve a connection request"""
        username, controller = self._setup(request)
        resp = controller.approve_connection(username)
        return CustomResponse(message=MSG, payload=resp, code=status.HTTP_200_OK)

    def delete(self, request):
        """remove a connection"""
        username, controller = self._setup(request)
        resp = controller.remove_connection(username)
        return CustomResponse(message=MSG, payload=resp, code=status.HTTP_200_OK)