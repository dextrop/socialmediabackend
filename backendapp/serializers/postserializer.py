import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backendapp.models import Post, Likes, Comments, Users
from backendapp.serializers.cacheserializer import CachedSerializer


class UsersSerializer(CachedSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username', 'profile_picture')

class LikeSerializer(CachedSerializer):
    liked_by = UsersSerializer()
    class Meta:
        model = Likes
        exclude = ('post_id', )


class CommentSerializer(CachedSerializer):
    commented_by = UsersSerializer()
    class Meta:
        model = Comments
        exclude = ('post_id', )


class PostSerializer(CachedSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

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
            raise ValidationError("Status doesn't looks safe, In status only alphanumeric charactersspaces, periods, commas, exclamation marks, percentage and question marks are allowed")

        return value

    def to_representation(self, instance):
        """Update each post with its like and comments"""
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(Likes.objects.filter(post_id=instance.id), many=True).data
        representation['comments'] = CommentSerializer(Comments.objects.filter(post_id=instance.id), many=True).data
        return representation
