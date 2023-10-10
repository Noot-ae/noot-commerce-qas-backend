from rest_framework.routers import DefaultRouter
from .views import PaymobGatewayViewSet, StripeGatewayViewSet, ActiveGateWayView, GetAvailablePaymentMethodView, CreatedGateWayView, CurrencyViewSet, GetCurrencyFactorsView
from django.urls import path

router = DefaultRouter()

router.register('paymob', PaymobGatewayViewSet)
router.register('stripe', StripeGatewayViewSet)
router.register('currency', CurrencyViewSet)

urlpatterns = [
    path('activated/', ActiveGateWayView.as_view()),
    path('factors/', GetCurrencyFactorsView.as_view()),
    path('available/', GetAvailablePaymentMethodView.as_view()),
    path('created/', CreatedGateWayView.as_view()),
] + router.urls
