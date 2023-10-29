from django.db import models
from backendapp.models import Users, Post

class Comments(models.Model):
    comment = models.CharField(max_length=255)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('comment', 'post_id', 'commented_by')
        db_table = 'comments'
        app_label = 'backendapp'
