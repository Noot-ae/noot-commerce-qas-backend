from rest_framework.viewsets import ModelViewSet
from ..models import Menu, MenuItem
from ..serializers import MenuItemSerializer, MenuSerializer
from utils.permissions import IsAdminOrReadOnly
from utils.mixins import CacheResponseMixin
from django.db.models import Prefetch
from django.db.models import F

class MenuItemViewSet(CacheResponseMixin, ModelViewSet):
    queryset = MenuItem.objects.all().prefetch_related('labels').annotate(
        category_slug = F("category__slug"),
        page_slug = F("page__slug")
    ).order_by('id')
    serializer_class = MenuItemSerializer
    filterset_fields = ['parent_item', 'menu', 'category', 'page']
    permission_classes = (IsAdminOrReadOnly,)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_root'] = True
        return context
    

class MenuViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Menu.objects.all().prefetch_related('names', Prefetch('menu_item_set', queryset=MenuItemViewSet.queryset)).order_by('id')
    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrReadOnly,)
    
        
