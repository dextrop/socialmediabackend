from backendapp.models import Post
from rest_framework.exceptions import ValidationError
from backendapp.serializers.commentsserializer import CommentsSerializer, Comments

class CommentController():
    def __init__(self, user):
        self.user = user

    def add_comment(self, post_id, comment):
        """ Check if Post exits for the provided post_id.
        If is found, create a new comment object """
        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            raise ValidationError("Post not found")

        Comments.objects.create(**{
            "comment": comment,
            "post_id": post,
            "commented_by": self.user
        })
        return True

    def get_user_comments(self):
        """ Get all comments made by a user in lifetime """
        comments = Comments.objects.filter(commented_by=self.user.id)
        return CommentsSerializer(comments, many=True).data

    def get_post_comments(self, post_id):
        """ Get all comments made on a post """
        comments = Comments.objects.filter(post_id=post_id)
        return CommentsSerializer(comments, many=True).data

    def remove_comments(self, comment_id):
        """ Remove a comment """
        comments = Comments.objects.filter(commented_by=self.user.id, id=comment_id)
        if not comments.exists():
            raise ValidationError("Comments does not exits")

        comments.delete()
        return True
