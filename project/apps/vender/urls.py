from rest_framework.routers import DefaultRouter
from .views import VenderOrdersViewset, VenderRegisterView, VenderListViewSet
from django.urls import path

router = DefaultRouter()
router.register('orders', VenderOrdersViewset)
router.register('get', VenderListViewSet)

urlpatterns = [
    path('register/', VenderRegisterView.as_view())    
] + router.urls
