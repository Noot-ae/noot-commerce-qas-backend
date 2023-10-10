from django.urls import path
from .views import TenantView, UpdateDestroyDomainView, GetCurrencyInfoView, OwnerTenantUpdateView, CurrencyFactorView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', TenantView)

urlpatterns = [
    path('currency/factors/', CurrencyFactorView.as_view()),
    path('domains/<str:slug>/', UpdateDestroyDomainView.as_view()),
    path('currency/', GetCurrencyInfoView.as_view()),
    path('owner/update/', OwnerTenantUpdateView.as_view(),)
] + router.urls

