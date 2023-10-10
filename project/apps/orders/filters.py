import django_filters as filters
from .models import Order

class DashboardOrderFilter(filters.FilterSet):
    region = filters.NumberFilter(field_name="shipment__region")
    country = filters.CharFilter(field_name="shipment__country", lookup_expr="icontains") 
    created_at_range = filters.DateFromToRangeFilter(field_name="created_at")
    created_at = filters.DateFilter(lookup_expr="date")
    
    class Meta:
        model = Order
        fields = ['payment_status', 'order_status', 'country', 'region', 'created_at', 'id']