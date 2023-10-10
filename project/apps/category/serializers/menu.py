from rest_framework.serializers import CharField
from ..models import Menu, MenuItem
from translations.serializers import TranslationSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer


class MenuItemSerializer(WritableNestedModelSerializer):
    labels = TranslationSerializer(many=True)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        if self.context.get('is_root', False):
            self.Meta.extra_kwargs = {}
    
    class Meta:
        model = MenuItem
        extra_kwargs = {"menu" : {"required" : False}}
        fields = '__all__'
        
    
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        extra_read_only = ['category_slug', 'page_slug']
        for value in extra_read_only:                
            try:
                data[value] = getattr(instance, value)
            except Exception as e:
                print(e)
                continue
        return data

class MenuSerializer(WritableNestedModelSerializer):
    names = TranslationSerializer(many=True)
    menu_item_set = MenuItemSerializer(many=True)
    page_slug = CharField(read_only=True)
    
    class Meta:
        model = Menu
        fields = ('id', 'names', 'menu_item_set', 'display_location', 'page_slug')


