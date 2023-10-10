from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, ListPreviousChatViewSet
from django.urls import path

router = DefaultRouter()

router.register('', ChatViewSet)

urlpatterns = [
    
    path('list/', ListPreviousChatViewSet.as_view()),

] + router.urls