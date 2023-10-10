import stripe
from rest_framework.exceptions import ParseError
from orders.models import Order, OrderProduct
from django.shortcuts import resolve_url, get_object_or_404
from django.views import View
from django.http import  HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from ..serializers import PaymentSerializer
from ..models import Payment, Refund
from rest_framework.response import Response
from django.db.transaction import atomic
from gateway.models.utils import StripeMixin
from ..permissions import CheckoutPermission

# Create your views here.

class StripeGatewayView(StripeMixin, CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (CheckoutPermission,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        self.set_stripe_secret()
        return super().post(request, *args, **kwargs)

    def serialize_order_items(self, order_products : list[OrderProduct]):
        return [
                {
                    "price_data": {
                        "currency": self.request.tenant.currency_code,
                        "unit_amount": int(op.get_total_pay_price()),
                        "product_data": {
                            "name": "purcashing credits",
                        },
                    },
                    "quantity": op.quantity,
                } for op in order_products
            ]
    
    def get_checkout_session(self):
        domain_url = f"{self.request.build_absolute_uri('/')[:-1]}"
        line_items = self.serialize_order_items(self.order.order_item_set.all())


        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            metadata={"order_id" : self.order.id, "amount" : self.order.get_total_pay_price()},
            mode="payment",
            success_url= self.stripe.PAYMENT_SUCCESS_URL(domain_url),
            cancel_url= self.stripe.PAYMENT_CANCEL_URL(domain_url),
        )
        return checkout_session

    def perform_create(self, serializer : PaymentSerializer):
        data : dict = serializer.validated_data
        self.order : Order = data['order']
        self.pay_amount = int(self.order.get_total_pay_price())
        checkout_session = self.get_checkout_session()
        self.url = resolve_url(checkout_session.url)
    
    def create(self, request, *args, **kwargs):
        response : Response = super().create(request, *args, **kwargs)
        response.data = {'url' : self.url}
        return response


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(StripeMixin, View):
    """
    Stripe webhook view to handle checkout session completed event.
    """
    def consruct_event(self, request):
        payload = request.body
        endpoint_secret = self.stripe.web_hook_secret
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return ParseError("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise ParseError("Invalid signature")
        except Exception as e:
            raise ParseError("something went wrong")

        return event

    def get_order(self, event):
        order_id = event["data"]["object"]['metadata']["order_id"]
        order = get_object_or_404(Order.objects.select_related('user', 'shipment', 'shipment__region'), id=order_id)
        return order

    def validate_order(self, event):
        self.order : Order = self.get_order(event)
        self.order.validate_quantity()

    @atomic()
    def post(self, request, format=None):
        event = self.consruct_event(request)
        if event["type"] == "checkout.session.completed":
            try:
                self.validate_order(event)
                return self.success(event)
            except Exception as e:
                self.refund(event)
        # Can handle other events here.
        return HttpResponse(status=200)
    
    def success(self, event):
        amount = self.order.get_total_pay_price()
        self.payment = Payment.objects.create(order=self.order, paid_amount=int(amount), user=self.order.user, transaction_id=event['data']['object']['payment_intent'])
        return HttpResponse(status=200)

    def cancel(self, event):
        return HttpResponse(status=403)
    
    def refund(self, event):
        payment_id = event['data']['object']['payment_intent']
        amount = event['data']['object']['metadata']['amount']
        stripe.PaymentIntent.retrieve(payment_id)
        Refund.objects.create(
            payment_intent=payment_id,
            refund_amount=int(float(amount)),
            order=self.order
        )
        return HttpResponse(status=400)

