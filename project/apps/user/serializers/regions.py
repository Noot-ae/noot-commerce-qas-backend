from drf_writable_nested.serializers import WritableNestedModelSerializer
from ..models import Region
from translations.serializers import TranslationSerializer

class RegionSerializer(WritableNestedModelSerializer):
    names = TranslationSerializer(many=True)
    
    class Meta:
        model = Region
        fields = '__all__'

