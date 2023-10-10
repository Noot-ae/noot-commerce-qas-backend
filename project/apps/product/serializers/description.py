from ..models import ProductDescription
from drf_writable_nested.serializers import WritableNestedModelSerializer
from translations.serializers import TranslationSerializer


class ProductDescriptionSerializer(WritableNestedModelSerializer):
    name = TranslationSerializer(many=True, required=False)
    description = TranslationSerializer(many=True, required=False)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        if self.context.get('is_root', False):
            self.Meta.extra_kwargs = {}
    
    class Meta:
        model = ProductDescription
        fields = '__all__'
        extra_kwargs = {
            "product" : {"required" : False}
        }