from rest_framework.viewsets import ModelViewSet
from ..models import ProductDescription
from utils.permissions import IsAdminOrReadOnly
from ..serializers import ProductDescriptionSerializer


class ProductDescriptionViewSet(ModelViewSet):
    queryset = ProductDescription.objects.all().prefetch_related(
        'name', 'description'
    )
    serializer_class = ProductDescriptionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['product_id']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_root'] = True
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(is_active=True)

