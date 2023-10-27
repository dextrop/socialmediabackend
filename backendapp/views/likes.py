from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from backendapp.serializers.likesserializer import Likes, LikesSerializer
from backendapp.models.post import Post
from backendapp.lib.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated

class LikeView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        post_id = request.GET.get("post_id")
        if post_id:
            likes = Likes.objects.filter(post_id=post_id)
            resp = LikesSerializer(likes, many=True).data
            return CustomResponse(message="Post API",payload=resp,code=status.HTTP_200_OK)
        else:
            likes = Likes.objects.filter(liked_by=request.user.id)
            resp = LikesSerializer(likes, many=True).data
            return CustomResponse(message="Post API",payload=resp,code=status.HTTP_200_OK)

    def post(self, request):
        post_id = request.data.get("post_id")
        if not post_id:
            raise ValidationError("Missing post id")
        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            raise ValidationError("Post not found")

        if Likes.objects.filter(liked_by=request.user.id, post_id=post_id).exists():
            raise ValidationError("Post already liked")

        Likes.objects.create(**{
            "post_id": post,
            "liked_by": request.user
        })
        return CustomResponse(message="Likes API", payload="Post liked", code=status.HTTP_201_CREATED)

    def delete(self, request):
        post_id = request.data.get("post_id")
        if not post_id:
            raise ValidationError("Missing post id")

        likes = Likes.objects.filter(liked_by=request.user.id, post_id=post_id)
        if not likes.exists():
            raise ValidationError("Post not liked")

        likes.delete()
        return CustomResponse(message="Likes API", payload="Post unliked", code=status.HTTP_201_CREATED)