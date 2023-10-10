from rest_framework.routers import DefaultRouter
from .views import PageCreateView, PageGetViewSet, TitleViewSet, SectionContentView, DestrySection, PageMetaViewSet
from django.urls import path

router = DefaultRouter()

router.register('get', PageGetViewSet)
router.register('content', SectionContentView)
router.register('title', TitleViewSet)
router.register('meta', PageMetaViewSet)

urlpatterns = [
  
  path('create/', PageCreateView.as_view()),
  path('section/<int:pk>/destroy/', DestrySection.as_view()),
  
] + router.urls
