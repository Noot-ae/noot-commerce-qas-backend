from .views import OverView, ProductViewSet, VariantDashViewSet, StatisticsView, TopProductsView
from user.views import OverViewShipmentView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('variant', VariantDashViewSet)
router.register("", ProductViewSet)

product_patterns = [
] + router.urls

reports_urls = [
    path('global', StatisticsView.as_view()),
]

urlpatterns = [
    path('shipment/', OverViewShipmentView.as_view()),
    path('reports/', include(reports_urls)),
    path('products/top/', TopProductsView.as_view()),
    path('products/', include(product_patterns)),
    path('', OverView.as_view()),
]
