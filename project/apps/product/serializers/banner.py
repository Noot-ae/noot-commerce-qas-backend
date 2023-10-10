from drf_writable_nested import WritableNestedModelSerializer
from ..models import Carousel, Banner
from translations.serializers import TranslationSerializer
from rest_framework import serializers
from page.models import Section

class BannerSerializer(WritableNestedModelSerializer):
    title = TranslationSerializer(many=True, required=False)
    sub_title = TranslationSerializer(many=True, required=False)
    content = TranslationSerializer(many=True, required=False)
    button_text = TranslationSerializer(many=True, required=False)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        if self.context.get('is_root', False):
            self.Meta.extra_kwargs = {}
        
    class Meta:
        model = Banner
        fields = '__all__'
        extra_kwargs = {
            "carousel" : {"required" : False}
        }


class CarouselSerializer(WritableNestedModelSerializer):
    banner_set = BannerSerializer(many=True)
    page = serializers.SlugRelatedField(queryset=Section.objects.all(), slug_field="slug")
    
    class Meta:
        model = Carousel
        fields = ('id', 'banner_set', 'slug', 'page', 'created_at')

