from rest_framework.viewsets import ModelViewSet
from ..models import Category
from ..serializers import CategorySerializer
from utils.permissions import IsAdminOrReadOnly
from ..filters import CategoryFilter
from utils.mixins import CacheResponseMixin
from django.db.models import Exists,Subquery, OuterRef
# Create your views here.

class CategoryViewSet(CacheResponseMixin, ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(
        has_sub_category = Exists(
            Subquery(
                Category.objects.filter(base_category_id=OuterRef('id'))
            )
        )    
    ).prefetch_related('names', 'descriptions')
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = CategoryFilter

