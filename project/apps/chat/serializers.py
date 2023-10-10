from rest_framework import serializers
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    # avatar = serializers.CharField(read_only=True, source="profile.avatar")
    last_message_text = serializers.CharField(read_only=True)
    last_message_date = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'last_message_text', 'last_message_date')


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {"message_status" : {"read_only": True}}
