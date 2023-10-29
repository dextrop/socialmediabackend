from backendapp.models import Post
from rest_framework.exceptions import ValidationError
from backendapp.serializers.likesserializer import LikesSerializer, Likes

class LikesController():
    def __init__(self, user):
        self.user = user

    def like_post(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            raise ValidationError("Post not found")

        if Likes.objects.filter(liked_by=self.user.id, post_id=post_id).exists():
            raise ValidationError("Post already liked")

        Likes.objects.create(**{
            "post_id": post,
            "liked_by": self.user
        })
        return True

    def unlike_post(self, post_id):
        likes = Likes.objects.filter(liked_by=self.user.id, post_id=post_id)
        if not likes.exists():
            raise ValidationError("Post not liked")

        likes.delete()
        return True


    def get_post_likes(self, post_id):
        likes = Likes.objects.filter(post_id=post_id)
        return LikesSerializer(likes, many=True).data

    def get_use_likes_activites(self):
        likes = Likes.objects.filter(liked_by=self.user.id)
        return LikesSerializer(likes, many=True).data
