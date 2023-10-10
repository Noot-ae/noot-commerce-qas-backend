from rest_framework.viewsets import ModelViewSet
from ..models import Region
from ..serializers import RegionSerializer
from utils.permissions import IsAdminOrReadOnly
from ..filters import RegionsFilter

class RegionViewSet(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = RegionsFilter

    def filter_queryset(self, queryset):
        if self.request.method != 'GET':
            return queryset
        return super().filter_queryset(queryset)
