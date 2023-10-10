from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from django.db import connection

channel_layer = get_channel_layer()

@receiver(post_save, sender=Message)
def after_message(sender: Message, instance : Message, **kwargs):
    async_to_sync(channel_layer.group_send)(
				f"{connection.schema_name}_user_{instance.receiver.id}",
				{'type': 'chat_message', 'message': MessageSerializer(instance=instance).data})

