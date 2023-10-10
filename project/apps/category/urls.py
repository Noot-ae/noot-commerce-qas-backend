from .views import CategoryViewSet, MenuViewSet, MenuItemViewSet 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('menu/item', MenuItemViewSet)
router.register('menu', MenuViewSet)
router.register('', CategoryViewSet)


urlpatterns = [] + router.urls