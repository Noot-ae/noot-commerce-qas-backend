from rest_framework import serializers
from .models import Section, SectionContent, Title, PageMeta
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from drf_writable_nested.serializers import WritableNestedModelSerializer


class PageMetaSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        if self.context.get('is_root', False):
            self.Meta.extra_kwargs = {}

    class Meta:
        model = PageMeta
        fields = '__all__'
        extra_kwargs = {
            "page" : {"required" : False}
        }



class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = SectionContent
        

class SectionContentCreateSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), write_only=True)
    
    def create(self, validated_data):
        page : Section = validated_data.pop('page')
        obj = super().create(validated_data)
        
        if self.context.get('add_to_field', 'content') == 'content':                
            page.content.add(obj)
        else:
            page.description.add(obj)
        page.save()
        return obj
    
    class Meta:
        fields = ('id', 'content', 'page', 'lang')
        model = SectionContent



class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
        extra_kwargs = {
            'section' : {"required" : False}
        }
    
    def validate(self, attrs):
        if self.context['request'].method == 'POST' and self.context.get("is_root", None) and not attrs.get('section'):
            raise ValidationError("section can't be blank", code='blank')
        return super().validate(attrs)


class SectionBaseSerializer(WritableNestedModelSerializer):
    
    title_set = TitleSerializer(many=True, required=False)
    content = SectionContentSerializer(many=True, required=False)
    description = SectionContentSerializer(many=True, required=False)

    class Meta:
        model = Section
        fields = ('id', 'title_set', 'content', 'description', 'thumbnail', 'section_type', 'slug', 'is_default')
        extra_kwargs = {
            'is_default' : {'read_only' : True}
        }

class SectionSerializer(SectionBaseSerializer):
    class Meta(SectionBaseSerializer.Meta):
        extra_kwargs = {
            "section_type" : {
                "required" : False,
                "default" : Section.PageSectionType.SECTION
            }
        }    


class PageSerializer(SectionBaseSerializer):
    page_section_set = SectionSerializer(many=True, required=False)
    page_meta = PageMetaSerializer(required=False)
    
    class Meta(SectionBaseSerializer.Meta):
        fields = SectionBaseSerializer.Meta.fields + ('page_section_set', 'page_meta')
        extra_kwargs = {
            'page' : {"read_only" : True},
            "section_type" : {
                "required" : False,
                "default" : Section.PageSectionType.PAGE
            }
        }    

    def create(self, validated_data: dict):
        try:                
            return super().create(validated_data)
        except IntegrityError as e:
            raise ValidationError(e, "slug_unique_error")
