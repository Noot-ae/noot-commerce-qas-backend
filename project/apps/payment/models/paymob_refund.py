from django.core.exceptions import ValidationError
import requests
from accept.endpoints import URLs

class PaymobRefundMixin:
    def get_paymob_api_key(self):
        return self.get_gateway().api_key

    def get_paymob_token(self):
        api_key = self.get_paymob_api_key()
        data = {'api_key': api_key}
        r = requests.post(self.urls.authentication_url(), json=data)
        if r.status_code > 201:
            raise ValidationError(f"Something went wrong, if you're site owner, please contact paymob provider {r.content}", code="gateway_invalid_config")
        token = r.json().get('token')
        if token is None:
            raise ValidationError(f"Something went wrong, if you're site owner, please contact paymob provider {r.content}", code="gateway_invalid_config")
        return token

    def do_paymob_refund(self):
        self.urls = URLs()
        account_token = self.get_paymob_token()
        data = {
            "auth_token": account_token,
            "transaction_id": self.payment_intent,
            "amount_cents": 1000
        }
        
        response = requests.post(self.urls.refund_transaction_url(), data)
        try:
            assert response.status_code == 201, response.content
        except AssertionError as e:
            raise ValidationError(e, code="invalid_refund_request")