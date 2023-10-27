# serializers.py
from rest_framework import serializers
from backendapp.models.connections import Connection

class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = '__all__'

