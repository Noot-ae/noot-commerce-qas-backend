from rest_framework.response import Response
from rest_framework import exceptions, views, generics
from user.serializers import ShipmentSerializer
from ..serializers import PaymobPaySerializer
from ..models import Payment
from accept.payment import *
from random import randrange
from ..permissions import CheckoutPermission
from .paymob_hmac_validator import HMACValidator
from django.shortcuts import get_object_or_404
from orders.models import Order
from gateway.models.utils import PaymobGateWayMixin
from .paymob_urls import CustomUrls

OrderData = lambda *args, **kwargs : {
    "auth_token": kwargs['auth_token'],
    "delivery_needed": "false",
    "amount_cents": kwargs['amount'],
    "currency": kwargs['currency'],
    "merchant_order_id": kwargs['merchant_order_id'],  # UNIQUE
    "items": args
}

Request = lambda **kwargs : {
    "auth_token": kwargs["auth_token"],
    "amount_cents": kwargs['amount'],
    "expiration": 3600,
    "order_id": kwargs['paymob_order'],
    "currency": "EGP",
    "integration_id": kwargs['integration_id'],  # https://accept.paymob.com/portal2/en/PaymentIntegrations
    "lock_order_when_paid": "false",
    "billing_data" : kwargs['billing_data']
}

class PaymobWebHook(PaymobGateWayMixin, views.APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def post(self, request):
        gateway_hmac = self.get_gateway().hmac_secret
        incoming_hmac = self.request.GET.get('hmac')
        if HMACValidator(incoming_hmac, request.data, site_hmac=gateway_hmac).is_valid:
            self.payment_verified()
        return Response({"hello" : "world"})

    def get_order_id(self):
        site_order_id = self.request.data.get('obj', {}).get('order', {}).get('merchant_order_id', None)
        if site_order_id is None:
            raise exceptions.ValidationError("can't access merchant_order_id")
        return site_order_id.split("-")[0]

    def get_order(self):
        return get_object_or_404(Order.objects.select_related('user', 'shipment', 'shipment__region'), id=self.get_order_id())

    def payment_verified(self):
        order = self.get_order()
        paid_amount_cents = self.request.data.get('obj', {}).get('order', {}).get('paid_amount_cents', None)
        Payment.objects.create(order=order, paid_amount=paid_amount_cents, transaction_id=self.request.data['order']['id'])


class PaymobGatewayView(PaymobGateWayMixin, generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymobPaySerializer
    permission_classes = (CheckoutPermission,)
    authentication_classes = []
    

    def post(self, request, *args, **kwargs):
        self.gateway = self.get_gateway()

        serializer = self.serializer_class
        serializer = serializer(data = request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        
        self.validated_data = serializer.validated_data
        self.validate_order()
        url = self.get_iframe_url()

        return Response({"url" : url})
    
    @property
    def merchant_order(self) -> Order:
        return self.validated_data['order']
    
    def validate_order(self):
        print("is paid", self.merchant_order.is_already_paid)
        if self.merchant_order.is_already_paid:
            raise exceptions.OrderSoldException()
    
    def get_iframe_url(self):
        self.api_key = self.gateway.api_key
        self.accept = AcceptAPI(self.gateway.api_key)
        self.accept.url = CustomUrls()
        self.paymob_order : dict = self.accept.order_registration(OrderData(*self.validated_data['serialized_order_items'], **self.get_order_data_kwargs()))

        payment_token = self.payment_key_request(Request(**self.get_payment_key_kwargs()))
        iframeURL = self.accept.retrieve_iframe(iframe_id=self.gateway.iframe_id, payment_token=payment_token)

        return iframeURL

    def get_order_data_kwargs(self):
        return {
            "auth_token" : self.retrieve_auth_token(),
            "amount" : self.merchant_order.get_total_pay_price(),
            "integration_id" : self.gateway.integration_id,
            "merchant_order_id" : f"{self.merchant_order.id}-{randrange(100_000_000)}",
            "currency" : self.gateway.currency
        }

    def get_payment_key_kwargs(self):
        return dict(**self.get_order_data_kwargs(), paymob_order = self.paymob_order.get('id'), billing_data = self.get_billing_data())

    def get_billing_data(self):
        return ShipmentSerializer(self.validated_data['profile']).data

   
    
