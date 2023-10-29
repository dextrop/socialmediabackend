from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from backendapp.controllers.likecontroller import LikesController
from backendapp.lib.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated

class LikeView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
            Get likes by post id or get all like activities by a user
        """
        post_id = request.GET.get("post_id")
        if post_id:
            resp = LikesController(request.user).get_post_likes(post_id)
        else:
            resp = LikesController(request.user).get_use_likes_activites()

        return CustomResponse( message="Post API", payload=resp, code=status.HTTP_200_OK )

    def post(self, request):
        """ Like a post """
        post_id = request.data.get("post_id")
        if not post_id:
            raise ValidationError("Missing post id")
        LikesController(request.user).like_post(post_id)
        return CustomResponse(message="Likes API", payload="Post liked", code=status.HTTP_201_CREATED)

    def delete(self, request):
        """Unlike a post previously liked"""
        post_id = request.data.get("post_id")
        if not post_id:
            raise ValidationError("Missing post id")
        LikesController(request.user).unlike_post(post_id)
        return CustomResponse(message="Likes API", payload="Post unliked", code=status.HTTP_201_CREATED)