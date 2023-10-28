from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from backendapp.serializers.commentsserializer import CommentsSerializer, Comments
from backendapp.models.post import Post
from backendapp.lib.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from backendapp.lib.helper import validate_request

class CommentView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        post_id = request.GET.get("post_id")
        if post_id:
            comments = Comments.objects.filter(post_id=post_id)
            resp = CommentsSerializer(comments, many=True).data
            return CustomResponse(message="Post API",payload=resp,code=status.HTTP_200_OK)
        else:
            comments = Comments.objects.filter(commented_by=request.user.id)
            resp = CommentsSerializer(comments, many=True).data
            return CustomResponse(message="Post API",payload=resp,code=status.HTTP_200_OK)

    def post(self, request):
        validate_request(
            request.data, ["post_id", "comment"]
        )
        try:
            post = Post.objects.get(id=request.data.get("post_id"))
        except Exception as e:
            raise ValidationError("Post not found")

        Comments.objects.create(**{
            "comment": request.data.get("comment"),
            "post_id": post,
            "commented_by": request.user
        })
        return CustomResponse(message="Comments API", payload="Comments Posted", code=status.HTTP_201_CREATED)

    def delete(self, request):
        comment_id = request.data.get("id")
        if not comment_id:
            raise ValidationError("Missing comment id")

        comments = Comments.objects.filter(commented_by=request.user.id, id=comment_id)
        if not comments.exists():
            raise ValidationError("Comments does not exits")

        comments.delete()
        return CustomResponse(message="Comments API", payload="Comments Deleted", code=status.HTTP_201_CREATED)