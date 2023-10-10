from django.forms import CharField
from django_filters import CharFilter, FilterSet
from .models import Post
from django.db.models import Q, QuerySet

class ContentFieldFilter(CharFilter):
    field_class = CharField

    def filter(self, qs : QuerySet, value):
        if not value: return qs
        return qs.filter(Q(title__text__icontains = value) | Q(body__text__icontains = value)).distinct()


class PostFilterSet(FilterSet):
    content = ContentFieldFilter()
    
    class Meta:
        model = Post
        fields = ("content", )