import django_filters
from .models import Category


class CategoryFilter(django_filters.FilterSet):
    is_base = django_filters.BooleanFilter(field_name="base_category", lookup_expr="isnull")
    
    class Meta:
        model = Category
        fields = ('is_base', 'id', 'slug', "base_category")