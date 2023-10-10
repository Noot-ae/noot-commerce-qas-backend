from gateway.models import Paymob
from rest_framework import exceptions
import requests
from django.utils.functional import cached_property
from gateway.models import Stripe
import stripe

class PaymobGateWayMixin:
    def get_gateway(self):
        try:
            gateway = Paymob.objects.get(is_active=True)
            return gateway
        except Paymob.DoesNotExist:
            raise exceptions.ValidationError("this site does not support paymob gateway", code="gateway_not_supported")

    def retrieve_auth_token(self):
        """
        Authentication Request:
        :return: token: Authentication token, which is valid for one hour from the creation time.
        """
        data = {'api_key': self.api_key}
        r = requests.post(self.accept.url.authentication_url(), json=data)
        if r.status_code > 201:
            raise exceptions.ValidationError(f"something went wrong {r.content}", code="gateway_invalid_config")
        token = r.json().get('token')
        return token
    
    def payment_key_request(self, data):
        r = requests.post(self.accept.url.payment_key_url(), json=data)
        if r.status_code > 201:
            raise exceptions.ValidationError(f"something went wrong {r.content}", code="gateway_invalid_config")
        payment_token = r.json().get('token')
        return payment_token

class StripeMixin:
    
    @cached_property
    def stripe(self) -> Stripe:
        stripe = Stripe.objects.filter(is_active=True).first()
        if stripe is None:
            raise exceptions.ValidationError("stripe is not active", code="gateway_not_supported")
        return stripe

    def set_stripe_secret(self):
        stripe.api_key = self.stripe.secret_key