from rest_framework.generics import UpdateAPIView
from user.permissions import IsSuperuser
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from .serializers import TenantSerializer, DomainSerializer, CurrencyInfoSerializer, TenantUpdateSerializer, TenantOwnerUpdateSerializer
from .models import Client, Domain
from django.db.transaction import atomic
from .permissions import IsTenantHandler
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.cache import get_base_currency_factors


class GetCurrencyInfoView(RetrieveAPIView):
    serializer_class = CurrencyInfoSerializer
    queryset = Client.objects.all()
    permission_classes = ()
    authentication_classes = ()
    
    def get_object(self):
        return self.request.tenant


class CurrencyFactorView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        return Response(
            {
                "factors" : get_base_currency_factors(request.tenant.currency_code)
            }
        )


class TenantView(UpdateModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (IsTenantHandler,)
    serializer_class = TenantSerializer
    queryset = Client.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        Client.objects.get(schema_name="public").activate()
        return super().dispatch(request, *args, **kwargs)

    @atomic
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TenantUpdateSerializer
        return super().get_serializer_class()
    
    
class OwnerTenantUpdateView(UpdateAPIView):
    serializer_class = TenantOwnerUpdateSerializer
    queryset = Client.objects.all()
    permission_classes = (IsSuperuser,)
    
    def get_object(self):
        return self.request.tenant


class UpdateDestroyDomainView(DestroyModelMixin, UpdateAPIView):
    queryset = Domain.objects.all()
    permission_classes = (IsTenantHandler,)
    serializer_class = DomainSerializer
    lookup_url_kwarg = "slug"
    lookup_field = "domain"
    
    def dispatch(self, request, *args, **kwargs):
        Client.objects.get(schema_name="public").activate()
        return super().dispatch(request, *args, **kwargs)
        
    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        serializer.Meta.fields = ('domain', 'is_primary')
        return serializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
