from django.db import models
from backendapp.models import Users

class Post(models.Model):
    status = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='uploads/', null=True, blank=True)
    posted_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('status', 'posted_by', 'picture')

