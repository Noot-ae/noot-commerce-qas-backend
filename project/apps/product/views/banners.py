from rest_framework.viewsets import ModelViewSet
from ..serializers import CarouselSerializer, BannerSerializer
from ..models import Carousel, Banner
from django.db.models import Prefetch
from utils.permissions import IsAdminOrReadOnly
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from django.db.transaction import atomic
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from utils.mixins import CacheResponseMixin

class CarouselViewSet(CacheResponseMixin, ModelViewSet):
    queryset = Carousel.objects.select_related('page').prefetch_related(
        Prefetch('banner_set', Banner.objects.prefetch_related('title', 'sub_title', 'content', 'button_text')), 'page__page_section_set'
    )
    serializer_class = CarouselSerializer
    permission_classes = (IsAdminOrReadOnly,)
    
    def _create(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer.data        

    @atomic
    def create(self, request, *args, **kwargs):
        if request.GET.get('delete_all'):
            Carousel.objects.all().delete()
        try:
            data = [self._create(_data) for _data in request.data]
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            raise ValidationError(code="unique")
        except ValueError as e:
            raise ValidationError(code="invalid")


class BannerViewSet(DestroyModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().prefetch_related('title', 'sub_title', 'content', 'button_text')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_root'] = True
        return context