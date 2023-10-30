from rest_framework import serializers
from backendapp.models import Users, Connection
from backendapp.serializers.cacheserializer import CachedSerializer


class SearchConnectionsSerializer(CachedSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        name = "users"
        model = Users
        fields = ('id', 'email', 'username', 'name', 'profile_picture')

    def to_representation(self, instance):
        """Update result with connection_status for each person, connection status can be
        Request_Sent, Connected, Wait for conformation
        """
        representation = super().to_representation(instance)
        user = self.context.get('user', None)  # Accessing the extra context

        send_connections = Connection.objects.filter(user=instance.id, connection=user.id)
        if send_connections.count() > 0:
            if send_connections[0].status == "Request_Sent":
                representation['connection_status'] = "Request Pending"
                return representation
            else:
                representation['connection_status'] = "Connected"
                return representation


        received_connections = Connection.objects.filter(connection=instance.id, user=user.id)
        if received_connections.count() > 0:
            if received_connections[0].status == "Request_Sent":
                representation['connection_status'] = "Wait for conformation"
                return representation
            else:
                representation['connection_status'] = "Connected"
                return representation
        return representation