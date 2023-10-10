from ..models import Paymob, Stripe
from rest_framework.views import APIView
from rest_framework.response import Response


class GetAvailablePaymentMethodView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        return Response(
            [
                {"gateway" : "paymob", "fields" : self.get_gateway_model_field_names(Paymob)},
                {"gateway" : "stripe", "fields" : self.get_gateway_model_field_names(Stripe)},
                
            ]
        )
    
    def get_gateway_model_field_names(self, model):
        return [f.name for f in model._meta.get_fields() if not f.blank]


