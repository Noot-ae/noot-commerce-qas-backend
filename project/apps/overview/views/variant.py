from product.views import ProductVariantViewSet
from .mixins import BaseViewMixin

class VariantDashViewSet(BaseViewMixin, ProductVariantViewSet):
    pass