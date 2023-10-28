from rest_framework.generics import ListAPIView
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from backendapp.lib.custompagination import CustomPagination
from backendapp.models import Users
from backendapp.serializers.searchconnectionsserializer import SearchConnectionsSerializer
from rest_framework.permissions import IsAuthenticated
from backendapp.serializers.userfilter import UserFilter
from backendapp.lib.custom_response import CustomResponse

class UserSearchAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Users.objects.all()
    serializer_class = SearchConnectionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    pagination_class = CustomPagination


    def get_queryset(self):
        # Exclude the authenticated user from the queryset
        return Users.objects.exclude(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_user = self.paginate_queryset(queryset)
        context = {'user': request.user}
        serializer = SearchConnectionsSerializer(paginated_user, many=True, context=context)
        resp = self.get_paginated_response(serializer.data)
        return CustomResponse(message="Users retrieved successfully", payload=resp, code=status.HTTP_200_OK)