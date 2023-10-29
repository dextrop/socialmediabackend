from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from backendapp.serializers.commentsserializer import CommentsSerializer, Comments
from backendapp.models.post import Post
from backendapp.lib.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from backendapp.controllers.commentscontroller import CommentController

class CommentView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """Get comments by post id or All comments by a user"""
        post_id = request.GET.get("post_id")
        if post_id:
            resp = CommentController(request.user).get_post_comments(post_id)
        else:
            resp = CommentController(request.user).get_user_comments()
        return CustomResponse(message="Post API", payload=resp, code=status.HTTP_200_OK)

    def post(self, request):
        """Comment for a post"""
        CommentController(request.user).add_comment(
            request.data.get("post_id"), request.data.get("comment")
        )
        return CustomResponse(message="Comments API", payload="Comments Posted", code=status.HTTP_201_CREATED)

    def delete(self, request):
        """delete a previosly posted comment"""
        comment_id = request.data.get("id")
        if not comment_id:
            raise ValidationError("Missing comment id")
        CommentController(request.user).remove_comments(comment_id)
        return CustomResponse(message="Comments API", payload="Comments Deleted", code=status.HTTP_201_CREATED)