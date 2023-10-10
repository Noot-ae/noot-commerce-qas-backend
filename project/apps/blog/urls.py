from rest_framework.routers import DefaultRouter
from .views import PostViewSet, SubscriptionCreateView
from django.urls import path

router = DefaultRouter()
router.register('', PostViewSet)

urlpatterns = [
    path('subscribe/', SubscriptionCreateView.as_view()),
    
] + router.urls