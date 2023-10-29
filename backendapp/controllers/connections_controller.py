from django.db.models import Q
from django.core.exceptions import ValidationError
from backendapp.serializers.connectionserializer import ConnectionSerializer, Connection
from backendapp.models import Users

class ConnectionsController():
    def __init__(self, user):
        self.user = user

    def get_all_connection(self):
        """List all connection for a user."""
        connectionObj = Connection.objects.filter(Q(user=self.user) | Q(connection=self.user))
        return ConnectionSerializer(connectionObj, many=True).data


    def add_connection(self, username):
        """Create a connection request"""
        try:
            connection_user = Users.objects.get(username=username)
        except Exception as e:
            raise ValidationError("User Does not exits")

        serializer = ConnectionSerializer(data={
            'user': self.user.id,
            'connection': connection_user.id
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return "Connection request send"

    def approve_connection(self, username):
        """Approve a connection request"""
        try:
            connection_user = Users.objects.get(username=username)
            connection_object = Connection.objects.get(user=connection_user.id, connection=self.user.id)
        except Exception as e:
            raise ValidationError("User Does not exits")

        print (connection_object.status)
        if (connection_object.status == "Blocked"):
            raise ValidationError("unable to approve connection request")

        if (connection_object.status == "Accepted"):
            raise ValidationError("request already accepted")

        setattr(connection_object, "status", "Accepted")
        connection_object.save()
        return "Connection Added Successfully"

    def remove_connection(self, username):
        """Remove a connection"""
        try:
            connection_user = Users.objects.get(username=username)
        except Exception as e:
            raise ValidationError("User Does not exits")

        obj = Connection.objects.filter(
                Q(user=self.user.id, connection=connection_user.id) |
                Q(user=connection_user.id, connection=self.user.id)
        )
        if obj.count() < 1:
            raise ValidationError("connection does not exits")

        obj.delete()
        return "Connection Removed Successfully"
