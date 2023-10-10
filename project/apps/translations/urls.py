from .views import TranslateView
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TranslationUpdateView

router = DefaultRouter()
router.register(r'update/(?P<translation_id>\d+)', TranslationUpdateView)

urlpatterns = [
    path('', TranslateView.as_view())
] + router.urls




