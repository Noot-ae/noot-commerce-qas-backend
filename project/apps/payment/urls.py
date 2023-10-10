from django.urls import path, include
from .views import StripeGatewayView, StripeWebhookView, PaymobGatewayView, PaymobWebHook

webhook_urls = [
    path('paymob/', PaymobWebHook.as_view()),
    path('stripe/', StripeWebhookView.as_view(), name="stripe-hook"),
]


urlpatterns = [
    path('stripe/', StripeGatewayView.as_view(), name="pay"),
    path('paymob/', PaymobGatewayView.as_view(), name="paymob"),
    path('webhooks/', include(webhook_urls))    
] 
