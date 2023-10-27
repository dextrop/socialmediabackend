from rest_framework import generics, status
from backendapp.serializers.postserializer import Post, PostSerializer
from backendapp.lib.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from backendapp.controllers.postcontroller import PostController

class PostView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        id = request.GET.get("id", None)
        if id is not None:
            posts = Post.objects.filter(id=id)
        else:
            posts = Post.objects.all()

        resp = PostSerializer(posts, many=True).data
        return CustomResponse(message="Post API",payload=resp,code=status.HTTP_200_OK)

    def post(self, request):
        status, error = PostController().create_post(request)
        if not status:
            return CustomResponse(message=error, payload=None, code=status.HTTP_400_BAD_REQUEST)
        return CustomResponse(message="Post API", payload="Post created Successfully", code=status.HTTP_201_CREATED)


    def delete(self, request):
        status = PostController().delete_post(request)
        return CustomResponse(message="Post API", payload="Post Deleted Successfully", code=status.HTTP_201_CREATED)