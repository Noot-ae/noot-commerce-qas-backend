from django.db.models import Sum
from orders.models import Order
from rest_framework.generics import GenericAPIView
from django_filters import FilterSet, filters
from payment.models import Refund
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from functools import cached_property
from .utils import BaseChartMixin
from rest_framework.serializers import Serializer

class FilterClass(FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()
    class Meta:
        fields = ['created_at']


class StatisticsView(BaseChartMixin, GenericAPIView):
    filterset_fields = ['created_at']
    queryset = Order.objects.all()
    serializer_class = Serializer
    permission_classes = []
    authentication_classes = []

    @method_decorator(cache_page(60*2))
    def get(self, request):
        results_keys = ['refunds', 'sales', 'net_sales', 'shipping']
        result = {}
        has_pre_qs = self.is_pre_available()
        for k in results_keys:
            name = f"total_{k}"
            result[name] = getattr(self, name)
            pre_name = f"pre_{name}"
            if has_pre_qs:
                try:
                    result[pre_name] = getattr(self, pre_name)
                except ValueError as e:
                    pass
            else:
                result[pre_name] = 0

        return Response(result)
    
    @cached_property
    def total_shipping(self):
        queryset = Order.objects.filter(payment_status=Order.PaymentStatus.PAID)
        queryset = queryset.aggregate(shipping_price=Sum("shipping_price"))
        return queryset['shipping_price'] or 0

    @cached_property
    def pre_total_shipping(self):
        queryset =  self.filter_pre_queryset(Order.objects.filter(payment_status=Order.PaymentStatus.PAID))
        queryset = queryset.aggregate(shipping_price=Sum("shipping_price"))
        return queryset['shipping_price'] or 0

    @cached_property
    def pre_total_sales(self):
        queryset =  self.filter_pre_queryset(Order.objects.filter(payment_status=Order.PaymentStatus.PAID))
        queryset = queryset.aggregate(total_amount=Sum("total_price"))
        return queryset['total_amount'] or 0
        
    @cached_property
    def pre_total_refunds(self):
        queryset = self.filter_pre_queryset(Refund.objects.all())
        queryset = queryset.aggregate(total_refunds = Sum("refund_amount"))
        return queryset['total_refunds'] or 0

    @cached_property
    def pre_total_net_sales(self):
        return self.pre_total_sales - self.pre_total_refunds

    @cached_property
    def total_sales(self):
        queryset =  self.filter_queryset(Order.objects.filter(payment_status=Order.PaymentStatus.PAID))
        queryset = queryset.aggregate(total_amount=Sum("total_price"))
        return queryset['total_amount'] or 0

    @cached_property
    def total_refunds(self):
        queryset = self.filter_queryset(Refund.objects.all())
        queryset = queryset.aggregate(total_refunds = Sum("refund_amount"))
        return queryset['total_refunds'] or 0

    @cached_property
    def total_net_sales(self):
        return self.total_sales - self.total_refunds
    

    