from ..serializers import StripeSerializer, PaymobSerializer
from ..models import Paymob, Stripe
from rest_framework.viewsets import ModelViewSet
from user.permissions import IsSuperuser
from rest_framework.views import APIView
from rest_framework.response import Response


class StripeGatewayViewSet(ModelViewSet):
    queryset = Stripe.objects.all()
    serializer_class = StripeSerializer
    permission_classes = (IsSuperuser,)
    

class PaymobGatewayViewSet(ModelViewSet):
    queryset = Paymob.objects.all()
    serializer_class = PaymobSerializer
    permission_classes = (IsSuperuser,)


class ActiveGateWayView(APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def get(self, request):
        self.active_gateways = []
        self.is_active_gateway(Stripe)
        self.is_active_gateway(Paymob)
        return Response(self.active_gateways)
    
    def is_active_gateway(self, model):
        try:
            assert model.objects.filter(is_active=True).exists()
            self.active_gateways.append(model.__name__.lower())
        except AssertionError:
            pass


class CreatedGateWayView(APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def get(self, request):
        self.active_gateways = []
        self.exists_gateway(Stripe)
        self.exists_gateway(Paymob)
        return Response(self.active_gateways)
    
    def exists_gateway(self, model):
        try:
            assert model.objects.filter(id__gte=0).exists()
            self.active_gateways.append(model.__name__.lower())
        except AssertionError:
            pass