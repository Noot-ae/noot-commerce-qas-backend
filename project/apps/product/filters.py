from django_filters import CharFilter, FilterSet, NumberFilter, DateFromToRangeFilter
from django.forms import IntegerField, CharField, SlugField
from category.models import Category
from .models import Product
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
import operator
from functools import reduce

class CategoryFieldFilter(CharFilter):
    field_class = SlugField

    def filter(self, qs: QuerySet, value):
        if not value: return qs
        try:                
            category : Category = Category.objects.get(slug=value)
        except Category.DoesNotExist:
            raise ValidationError({"category_tree":"Parent category does not exist"})
        cat_qs = category.get_descendants(include_self=True)
        return qs.filter(category__in = cat_qs)


class InStockFieldFilter(NumberFilter):
    field_class = IntegerField
    
    def filter(self, qs, value):
        if not value: return qs        

        filter_kwargs = {}
        if value: filter_kwargs['product_variant_set__quantity__gte'] = value
        return qs.filter(**filter_kwargs)


class ContentFieldFilter(CharFilter):
    field_class = CharField

    def filter(self, qs, value : str):
        if not value: return qs
        
        filter_lookup = lambda name : reduce(operator.or_, (Q(**{f"{name}__text__icontains":x}) for x in value.split()))
        
        return qs.filter(
            Q(
                filter_lookup("name")    
            ) | Q(
                filter_lookup("description")
            )
        )
    

class ProductFilterSet(FilterSet):
    category_tree = CategoryFieldFilter()
    content = ContentFieldFilter()
    price = NumberFilter(field_name='product_variant_set__price')
    price__gt = NumberFilter(field_name='product_variant_set__price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='product_variant_set__price', lookup_expr='lt')
    price__gte = NumberFilter(field_name='product_variant_set__price', lookup_expr='gte')
    price__lte = NumberFilter(field_name='product_variant_set__price', lookup_expr='lte')
    
    discount = NumberFilter(field_name='product_variant_set__discount')
    discount__gt = NumberFilter(field_name='product_variant_set__discount', lookup_expr='gt')
    discount__lt = NumberFilter(field_name='product_variant_set__discount', lookup_expr='lt')
    discount__gte = NumberFilter(field_name='product_variant_set__discount', lookup_expr='gte')
    discount__lte = NumberFilter(field_name='product_variant_set__discount', lookup_expr='lte')
    created_at = DateFromToRangeFilter()
    stock = InStockFieldFilter()
    category = CharFilter(field_name="category__slug", lookup_expr="icontains")
    
    class Meta:
        model = Product
        fields = ('category_tree', 'category', 'content', 'price', 'discount', 'slug', 'created_at', 'stock')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        filter_kwargs = {}
        # for q in self.request.GET:
        #     if not q.startswith("_"): continue            
        #     filter_kwargs[f"product_variant_set__sku__attribute_value"] = self.request.GET[q]
        #     filter_kwargs[f"product_variant_set__sku__attribute__name__icontains"] = q[1:]
        queryset = queryset.filter(**filter_kwargs)
        queryset = self.sort_queryset(queryset)
        return queryset
    
    def sort_queryset(self, queryset):
        ordering_data = {
            "highest_rate" : "-total_rating",
            "lowset_rate" : "total_rating",
            "highest_price" : "-price",
            "lowest_price" : "price",
        }
        
        if not self.request.GET.get("sorting", False) in ordering_data: return queryset

        try:                
            queryset = queryset.order_by(ordering_data[self.request.GET['sorting']])
        except KeyError as e:
            pass
        return queryset


