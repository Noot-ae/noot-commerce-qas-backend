from utils.permissions import IsAdminOrReadOnly
from rest_framework.viewsets import ModelViewSet
from ..models import Attribute, VariantAttribute, AttributeValue
from ..serializers import VarientAttributeSerializer, VriantUpdateAttributeSerializer, AttributeValueSerializer
from .mixins import CustomCreateDeleteViewMixin
from rest_framework.views import APIView
from utils.mixins import CacheResponseMixin


class AttributeViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Attribute.objects.all().prefetch_related("attribute_value_set")
    serializer_class = VarientAttributeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AttributeValueViewSet(ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['attribute_id']


class VariantAttributeView(CustomCreateDeleteViewMixin, APIView):
    serializer_class = VriantUpdateAttributeSerializer
    queryset = VariantAttribute.objects.all()
    create_key = "variant_attribute_set"
    
    