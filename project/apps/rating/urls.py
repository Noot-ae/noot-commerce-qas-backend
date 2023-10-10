from rest_framework.routers import DefaultRouter
from .views import ProductRatingViewSet, ProductReplyViewSet, LikeViewSet
from django.urls import path

router = DefaultRouter()

router.register('product', ProductRatingViewSet)
router.register('reply', ProductReplyViewSet)

urlpatterns = [
    path('likes/<str:model_name>/<int:pk>/<str:action>/', LikeViewSet.as_view()),
    
] + router.urls
