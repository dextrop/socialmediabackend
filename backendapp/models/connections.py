from django.db import models
from backendapp.models import Users
from django.core.exceptions import ValidationError

class Connection(models.Model):
    REQUEST_SENT = 'Request_Sent'
    ACCEPTED = 'Accepted'

    STATUS_CHOICES = [
        (REQUEST_SENT, 'Request Sent'),
        (ACCEPTED, 'Accepted')
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_connections')
    connection = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='connection_requests')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=REQUEST_SENT)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Connection, self).save(*args, **kwargs)


    class Meta:
        unique_together = ('user', 'connection')
