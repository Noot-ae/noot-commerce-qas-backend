from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product
from orders.models import Order
from user.models import User
from payment.models import Payment
from django.db.models import Sum, Avg
from django.utils import timezone
from vender.models import Vender
from rating.models import VenderRating, ProductRating
from .mixins import BaseViewMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


def get_current_date():
    current_date = timezone.now()  # Get the current date and time in the default timezone
    current_month = current_date.month
    current_year = current_date.year
    return {
        'current_date' : current_date, 'current_month' : current_month, 'current_year' : current_year, 'last_month' : (current_month - 1),
        'current_day' : current_date.date()
    }

# Create your views here.
class OverView(BaseViewMixin, APIView):
    
    @method_decorator(cache_page(60*2))
    def get(self, request):
        return Response(
            dict(
            **{
                'total_venders' : self.model_counts(Vender),
                'total_products' : self.model_counts(Product), 
                'total_orders' : self.model_counts(Order),
                'total_users' : self.model_counts(User),
                'orders_underway' : Order.objects.filter(order_status = Order.OrderStatus.shipped).count()
            }, 
            **self.payment_overview(),
            **{'rating' : self.rating_overview()}
            )
        )
    
    def rating_overview(self):
        product_rating = ProductRating.objects.aggregate(Avg('rate'))['rate__avg']
        vender_rating = VenderRating.objects.aggregate(Avg('rate'))['rate__avg']
        return {
            'products' : product_rating,
            'venders' : vender_rating
        }
        
    def payment_overview(self):
        self.current_date = get_current_date() 
        return {
            "current_month" : (Payment.objects.filter(
                paid_at__month=self.current_date['current_month'], 
                paid_at__year=self.current_date['current_year']
            ).aggregate(Sum("paid_amount"))['paid_amount__sum'] or 0),
            
            "last_month" : (Payment.objects.filter(
                paid_at__month=self.current_date['last_month'], 
                paid_at__year=self.current_date['current_year']
            ).aggregate(Sum("paid_amount"))['paid_amount__sum'] or 0),
            
            "current_day" : (Payment.objects.filter(
                paid_at__date=self.current_date['current_day'], 
            ).aggregate(Sum("paid_amount"))['paid_amount__sum'] or 0),
            
            "total_payments" : (Payment.objects.all().aggregate(Sum("paid_amount"))['paid_amount__sum'] or 0),
        }
        
    def model_counts(self, model):
        return model.objects.count()


