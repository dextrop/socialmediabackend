from django.db import models
from backendapp.models import Post, Users

class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

