from rest_framework.exceptions import ValidationError
from backendapp.models import Post
from backendapp.serializers.postserializer import PostSerializer


class PostController():
    def get_all_post(self, request):
        id = request.GET.get("id", None)
        if id is not None:
            posts = Post.objects.filter(posted_by=request.user.id, id=id)
        else:
            posts = Post.objects.filter(posted_by=request.user.id)

        return PostSerializer(posts, many=True).data

    def create_post(self, request):
        request_data = request.data.dict()
        request_data["posted_by"] = request.user.id
        serializer = PostSerializer(data=request_data)
        if serializer.is_valid():
            post_data = serializer.validated_data
            Post.objects.create(**post_data)
            return True, None
        return False, serializer.errors

    def delete_post(self, request):
        postObj = Post.objects.filter(id=request.data.get("id"), posted_by=request.user.id)
        if postObj.count() < 1:
            raise ValidationError("Post not found")
        postObj.delete()
        return True