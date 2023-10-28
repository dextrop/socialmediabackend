from rest_framework import serializers
from backendapp.models import Post, Likes, Comments, Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('name', 'username', 'profile_picture')

class LikeSerializer(serializers.ModelSerializer):
    liked_by = UsersSerializer()
    class Meta:
        model = Likes
        exclude = ('post_id', )


class CommentSerializer(serializers.ModelSerializer):
    commented_by = UsersSerializer()
    class Meta:
        model = Comments
        exclude = ('post_id', )


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(Likes.objects.filter(post_id=instance.id), many=True).data
        representation['comments'] = CommentSerializer(Comments.objects.filter(post_id=instance.id), many=True).data
        return representation
