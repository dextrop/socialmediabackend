from rest_framework.generics import ListAPIView
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
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

    def get_queryset(self):
        # Exclude the authenticated user from the queryset
        return Users.objects.exclude(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        context = {'user': request.user}
        serializer = SearchConnectionsSerializer(queryset, many=True, context=context)
        return CustomResponse(message="Users retrieved successfully", payload=serializer.data, code=status.HTTP_200_OK)