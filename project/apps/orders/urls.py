from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderProductViewSet, DashBoardOrderViewSet, CancelOrderView, GuestOrderViewSet
from django.urls import path


router = DefaultRouter()

router.register('vendor', OrderProductViewSet)
router.register('guest', GuestOrderViewSet)
router.register('dashboard', DashBoardOrderViewSet)
router.register('', OrderViewSet)

urlpatterns = [
        path('cancel/<int:pk>/', CancelOrderView.as_view()),
] + router.urls