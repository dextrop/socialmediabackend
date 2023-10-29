from rest_framework import generics, status
from backendapp.serializers.postserializer import Post, PostSerializer
from backendapp.middlewares.custom_response import CustomResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from backendapp.controllers.postcontroller import PostController
from backendapp.middlewares.custompagination import CustomPagination

class PostView(generics.GenericAPIView):
    allowed_methods = ("POST",)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination

    def get(self, request):
        """Return all post by user or return post by ID"""
        id = request.GET.get("id", None)
        if id is not None:
            posts = Post.objects.filter(id=id)
        else:
            posts = Post.objects.all()

        # Applying pagination
        paginated_posts = self.paginate_queryset(posts)
        serializer = PostSerializer(paginated_posts, many=True)

        # If you want to return pagination controls, you can return paginated response
        resp = self.get_paginated_response(serializer.data)
        return CustomResponse(message="Post API",payload=resp,code=status.HTTP_200_OK)

    def post(self, request):
        """Create a new post"""
        status, error = PostController().create_post(request)
        if not status:
            return CustomResponse(message=error, payload=None, code=status.HTTP_400_BAD_REQUEST)
        return CustomResponse(message="Post API", payload="Post created Successfully", code=status.HTTP_201_CREATED)


    def delete(self, request):
        """Delete Created post"""
        status = PostController().delete_post(request)
        return CustomResponse(message="Post API", payload="Post Deleted Successfully", code=status.HTTP_201_CREATED)