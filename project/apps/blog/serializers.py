from rest_framework import serializers
from .models import Post, Subscription
from drf_writable_nested.serializers import WritableNestedModelSerializer
from translations.serializers import TranslationSerializer

class PostSerializer(WritableNestedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = TranslationSerializer(many=True)
    body = TranslationSerializer(many=True)
    
    class Meta:
        model = Post
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
