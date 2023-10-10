from rest_framework import serializers
from .models import Translation

class TranslationSerializer(serializers.ModelSerializer):

    lang_type_display = serializers.CharField(read_only=True, source="get_lang_type_display")

    class Meta:
        model = Translation
        fields = ('id', 'is_ltr', 'text', 'lang', 'lang_type_display')


class TranslateSerializer(serializers.Serializer):
    destination = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    
    class Meta:
        fields = ('destination', 'text')