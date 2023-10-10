from ..serializers import CurrencySerializer
from ..models import Currency
from rest_framework.viewsets import ModelViewSet
from utils.permissions import IsAdminOrReadOnly
from utils.mixins import CacheResponseMixin


# Create your views here.
class CurrencyViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAdminOrReadOnly,)
    