from rest_framework.routers import DefaultRouter
from product.views import CarouselViewSet, BannerViewSet
from .views import ExportView
from django.urls import path

router = DefaultRouter()
router.register('carousel', CarouselViewSet)
router.register('banner', BannerViewSet)

urlpatterns = [
    path("export", ExportView.as_view()),
] + router.urls
