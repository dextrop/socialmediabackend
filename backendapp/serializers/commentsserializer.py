import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from backendapp.models import Comments

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

    def validate_comment(self, value):
        """
        Verify the status is safe.
        - Allows alphanumeric characters.
        - Allows spaces, periods, commas, exclamation marks, percentage and question marks.
        - Does not allow any other special characters or symbols.
        """

        # Regex pattern to match allowed characters
        pattern = r"^[a-zA-Z0-9\s\.,!?%]*$"

        if not re.fullmatch(pattern, value):
            raise ValidationError("Status doesn't looks safe, In status only alphanumeric charactersspaces, periods, commas, exclamation marks, percentage and question marks are allowed")

        return value



