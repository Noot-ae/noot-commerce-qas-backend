from rest_framework import serializers
from ..models import Category
from translations.serializers import TranslationSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer


class HasSubCategoryMixin(serializers.ModelSerializer):
    has_sub_category = serializers.BooleanField(read_only=True)
    
    class Meta:
        abstract = True
        
    def get_field_names(self, declared_fields, info):
        return super().get_field_names(declared_fields, info) + ('has_sub_category',)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(HasSubCategoryMixin, WritableNestedModelSerializer):
    sub_categories = SubCategorySerializer(many=True, write_only=True)
    names = TranslationSerializer(many=True)
    descriptions = TranslationSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'names', 'descriptions', 'sub_categories', 'base_category', 'slug', 'thumbnail', 'created_at', 'icon')


