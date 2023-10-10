from django.db import models
from django.conf import settings

# Create your models here.

class Message(models.Model):
    
    class MessageStatus(models.IntegerChoices):
        sent = 1, "sent"
        received = 2, "received"
        is_seen = 3, "seen"

    sender = models.ForeignKey("user.User", models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey("user.User", models.CASCADE, related_name='received_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=512)
    message_status = models.IntegerField(choices=MessageStatus.choices, default=MessageStatus.sent) 

