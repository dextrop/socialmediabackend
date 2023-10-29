from rest_framework.generics import ListAPIView
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from backendapp.middlewares.custompagination import CustomPagination
from backendapp.middlewares.logginmixin import LoggingMixin
from backendapp.models import Users
from backendapp.serializers.searchconnectionsserializer import SearchConnectionsSerializer
from rest_framework.permissions import IsAuthenticated
from backendapp.serializers.userfilter import UserFilter
from backendapp.middlewares.custom_response import CustomResponse

class UserSearchAPIView(ListAPIView, LoggingMixin):
    permission_classes = (IsAuthenticated, )
    queryset = Users.objects.all()
    serializer_class = SearchConnectionsSerializer
    filter_backends = [DjangoFilterBackend]

    # Pagination class
    pagination_class = CustomPagination

    # custom filter for searching names, username and email
    # whereas name is searched using LIKE sql query.
    filterset_class = UserFilter



    def get_queryset(self):
        # This function modifies the queryset to exclude the authenticated user.
        return Users.objects.exclude(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        """
        This function handles the GET request, applies filtering and pagination to the queryset,
        serializes it, and returns a custom response with a message and paginated data.
        """
        queryset = self.filter_queryset(self.get_queryset())
        paginated_user = self.paginate_queryset(queryset)
        context = {'user': request.user}
        serializer = SearchConnectionsSerializer(paginated_user, many=True, context=context)
        resp = self.get_paginated_response(serializer.data)
        return CustomResponse(message="Users retrieved successfully", payload=resp, code=status.HTTP_200_OK)