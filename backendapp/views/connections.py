from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from backendapp.lib.custom_response import CustomResponse
from backendapp.controllers.connections_controller import ConnectionsController

class ConnectionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        controller = ConnectionsController(request.user)
        return CustomResponse(
            message="Connections API",
            payload=controller.get_all_connection(),
            code=status.HTTP_200_OK
        )

    def post(self, request):
        controller = ConnectionsController(request.user)
        return CustomResponse(
            message="Connections API",
            payload=controller.add_connection(request.data.get("username", None)),
            code=status.HTTP_200_OK
        )

    def put(self, request):
        action = request.data.get('action')
        controller = ConnectionsController(request.user)
        if action == "block":
            return CustomResponse(
                message="Connections API",
                payload=controller.block_connection(request.data.get("username", None)),
                code=status.HTTP_200_OK
            )
        else:
            return CustomResponse(
                message="Connections API",
                payload=controller.approve_connection(request.data.get("username", None)),
                code=status.HTTP_200_OK
            )

    def delete(self, request):
        controller = ConnectionsController(request.user)
        return CustomResponse(
            message="Connections API",
            payload=controller.remove_connection(request.data.get("username", None)),
            code=status.HTTP_200_OK
        )
