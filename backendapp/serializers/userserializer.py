import re
from rest_framework import serializers
from backendapp.models import Users
from backendapp.serializers.cacheserializer import CachedSerializer

class UsersSerializer(CachedSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        name = "users"
        model = Users
        fields = ('id', 'email', 'username', 'name', 'profile_picture', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Password must be a write only field.

    def validate_password(self, value):
        """Validate Password"""
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least 1 uppercase letter.')

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least 1 lowercase letter.')

        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Password must contain at least 1 number.')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('Password must contain at least 1 special character.')

        return value

    def validate_username(self, value):
        """
        Validate the username to ensure it meets the necessary criteria,
        such as not containing any special characters.
        """
        if not value.isalnum():
            raise serializers.ValidationError("Username should only contain alphanumeric characters.")
        return value

