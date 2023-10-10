from .views import ProductsView, ProductVariantViewSet, UpdateDeleteProductView, ProductCreateView, AttributeViewSet, ProductImageView, VariantAttributeView, CartViewSet,MyProductsView, WishItemViewSet, AttributeValueViewSet, ProductDescriptionViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()

router.register('descriptions', ProductDescriptionViewSet)
router.register('attribute/value', AttributeValueViewSet)
router.register('attribute', AttributeViewSet)
router.register('cart', CartViewSet)
router.register('my', MyProductsView)
router.register('wish', WishItemViewSet)
router.register('variant', ProductVariantViewSet)
router.register('', ProductsView)

urlpatterns = [
    path('change/<int:pk>/', UpdateDeleteProductView.as_view()),
    path('variants/attribute/', VariantAttributeView.as_view()),
    path('variants/images/', ProductImageView.as_view()),
    path('create/', ProductCreateView.as_view()),
] + router.urls