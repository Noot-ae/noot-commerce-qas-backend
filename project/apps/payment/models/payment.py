from django.db import models
import stripe
from gateway.models.utils import PaymobGateWayMixin, StripeMixin
from .paymob_refund import PaymobRefundMixin

class Payment(models.Model):
    class GateWayChoices(models.TextChoices):
        PAYMOB = "PAYMOB"
        STRIPE = "STRIPE"
        
    order = models.ForeignKey('orders.Order', models.SET_NULL, null=True)
    paid_amount = models.FloatField()
    paid_at = models.DateTimeField(auto_now_add=True)
    gateway = models.CharField(max_length=12, choices=GateWayChoices.choices)
    transaction_id = models.CharField(max_length=256)
    

class Refund(PaymobGateWayMixin, PaymobRefundMixin, StripeMixin, models.Model):

    order = models.ForeignKey('orders.Order', models.CASCADE)
    payment = models.ForeignKey(Payment, models.CASCADE, null=True)
    
    refund_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent = models.CharField(max_length=256)

    def do_refund(self):
        if self.is_stripe():
            self.do_stripe_refund()

        elif self.payment.gateway == Payment.GateWayChoices.PAYMOB:
            self.do_paymob_refund()

    def is_stripe(self):
        return any([not self.payment_id, self.payment.gateway == Payment.GateWayChoices.STRIPE])
        

    def do_stripe_refund(self):
        self.set_stripe_secret()
        stripe.Refund.create(
                payment_intent=self.payment_intent,
                amount=int(self.refund_amount),
        )
        