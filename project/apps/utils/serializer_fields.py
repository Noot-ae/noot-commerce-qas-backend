from rest_framework.serializers import SlugRelatedField

class CurrentUserRelatedField(SlugRelatedField):
    
    def __init__(self, slug_field="id", user_field="user", **kwargs):
        self.user_field = user_field
        super().__init__(slug_field, **kwargs)
        
    def get_queryset(self):
        qs = super().get_queryset()    
        qs = qs.filter(**{self.user_field : self.context['request'].user} ) 
        return qs


class StringCurrentUserRelatedField(CurrentUserRelatedField):
    
    def to_representation(self, obj):
        data = super().to_representation(obj)
        return str(data)