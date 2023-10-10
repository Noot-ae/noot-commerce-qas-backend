from django.db import models
from .exceptions import OrderSoldException
from utils.get_current_tenant import get_current_tenant
from rest_framework.exceptions import ValidationError
from payment.models import Refund, Payment
from utils.price_converter import price_converter

# Create your models here.
class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = "Paid"
        REFUNDED = "Refunded"
        PENDING = "Pending"
        PARTIALLY_REFUNDED = "Partially Refunded"
        ON_HOLD = "On Hold"
        COMPLETED = "Completed"
        CANCELLED = "CANCELLED"
        PROCESSING = "Processing"


    class OrderStatus(models.TextChoices):
        processing = "Processing"
        placed = "PLACED"
        shipped = "SHIPPED"
        received = "RECEIVED"
        cancelled = "CANCELLED"

    payment_status = models.CharField(choices=PaymentStatus.choices, max_length=64, default=PaymentStatus.PENDING)
    order_status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.processing, max_length=32)
    order_currency_code = models.CharField(max_length=9)
    order_notes = models.CharField(max_length=512, blank=True, null=True)
    
    shipment = models.ForeignKey("user.ShipmentProfile", models.CASCADE, null=True, blank=False)
    
    shipping_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)
    promo_codes = []
    
    def validate(self):
        self.validate_min_price(self.total_price)
        self.validate_quantity()
        
    def validate_min_price(self, price):
        min_price = self.shipment.region.minimum_order_price
        if price < min_price:
            currency_code = self.shipment.region.currency_code
            raise ValidationError(f"order can't be less than {min_price} {currency_code}", code="invalid_order_min_price")
            
    def validate_quantity(self):
        for product in self.get_order_product_set():
            product.validate_product_quantity()

    def get_order_product_set(self):
        return self.order_item_set.all()
    
    def get_order_items_total_price(self):
        total_price = 0
        for item in self.get_order_product_set():
            total_price += item.total_price
        return total_price        
    
    def set_total_prices(self):
        "price returned in cents"
        total_price = self.get_order_items_total_price()
        self.validate_min_price(total_price)
        
        self.total_price = total_price
        self.total_price = price_converter(self.total_price)
        
        self.set_shipping_price()
        self.save(update_fields=['total_price'])
    
    def activate_order(self):
        for product in self.get_order_product_set():
            product.reduce_product_quantity()
        self.payment_status = self.__class__.PaymentStatus.PAID
        self.save(update_fields=["payment_status"])

    def cancel_order(self):
        self.order_status = self.__class__.OrderStatus.cancelled
        self.payment_status = self.__class__.PaymentStatus.REFUNDED
        self.save(update_fields=['order_status', 'payment_status'])        
        self.create_refund()
        self.update_refunded_variants()

    def create_refund(self):
        payment : Payment = self.payment_set.first()        
        try:                
            Refund.objects.create(
                payment=payment,
                order=self,
                refund_amount = self.total_price,
                payment_intent = payment.transaction_id
            )
        except Exception as e:
            raise ValidationError(e, code="refund_error")

    def update_refunded_variants(self):
        for order_product in self.get_order_product_set():
            order_product.product_variant.change_quantity(order_product.quantity)

    def set_shipping_price(self):
        self.shipping_price = self.shipment.region.get_order_shipment_price(self.total_price)

    def get_total_pay_price(self):
        return self.total_price + self.shipping_price

    @property
    def price_cents(self):
        return self.total_price * 100


class OrderProduct(models.Model):

    order = models.ForeignKey('orders.Order', models.CASCADE, related_name="order_item_set")
    product_variant = models.ForeignKey('product.ProductVariant', models.PROTECT, related_name="as_order_item_set")
    quantity = models.IntegerField()
    price = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_codes = []
            
    def save(self, *args, **kwargs):
        if (not self.price):
            self.set_price()
        return super().save(*args, **kwargs)    

    def set_price(self):
        total_prices = 0
        total_prices += self.product_variant.price * self.quantity
        for promo_code in self.promo_codes:
            pass

        self.price = total_prices
    
    def validate_product_quantity(self):
        if not self.product_variant.quantity >= self.quantity:
            raise OrderSoldException(f"product {self} has been sold")
        
    def reduce_product_quantity(self):
        self.validate_product_quantity()
        self.product_variant.reduce_quantity(self.quantity)

    @property
    def total_price(self):
        if not self.price:
            self.set_price()
        return self.price
    
