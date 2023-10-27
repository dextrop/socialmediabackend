import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backendapp.models import Post

class PostSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'status', 'picture', 'posted_by', 'date_created', 'date_modified')

    def validate_status(self, value):
        """
        Verify the status is safe.
        - Allows alphanumeric characters.
        - Allows spaces, periods, commas, exclamation marks, percentage and question marks.
        - Does not allow any other special characters or symbols.
        """

        # Regex pattern to match allowed characters
        pattern = r"^[a-zA-Z0-9\s\.,!?%]*$"

        if not re.fullmatch(pattern, value):
            raise ValidationError("status doesn't looks safe, In status only alphanumeric charactersspaces, periods, commas, exclamation marks, percentage and question marks are allowed")

        return value



