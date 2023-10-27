# serializers.py
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from backendapp.models import Users
from backendapp.models.connections import Connection

class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = '__all__'

    def validate(self, data):
        user = data.get("user")
        connection_user = data.get("connection")

        if Connection.objects.filter(
                Q(user=user, connection=connection_user) |
                Q(user=connection_user, connection=user)
        ).exists():
            print("In Validated")
            raise ValidationError('Connection already exists.')

        return data
