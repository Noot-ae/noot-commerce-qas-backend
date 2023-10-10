from rest_framework.viewsets import ModelViewSet
from ..serializers import WishItemSerializer
from ..models import WishItem
from utils.decorators import get_queryset_wrapper

class WishItemViewSet(ModelViewSet):
    queryset = WishItem.objects.all().select_related('product', 'product__product').prefetch_related(
        'product__variant_image_set',
        'product__product__name'
    )
    serializer_class = WishItemSerializer
    
    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs.select_related('user')
        return qs.filter(user_id =self.request.user.id)
    
    def get_serializer_context(self, **kwargs):
        context = super().get_serializer_context(**kwargs)
        context["is_superuser"] = self.request.user.is_superuser
        return context
        