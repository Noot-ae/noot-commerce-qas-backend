from .mixins import CustomCreateDeleteViewMixin
from rest_framework.views import APIView
from ..models import ProductImage
from ..serializers import ProductImageCreateSerializer

class ProductImageView(CustomCreateDeleteViewMixin, APIView):
    serializer_class = ProductImageCreateSerializer
    queryset = ProductImage.objects.all()
    create_key = "images"
    