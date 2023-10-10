from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from .models import Section, SectionContent, Title, PageMeta
from django.db.models import Prefetch
from .serializers import PageSerializer, TitleSerializer, SectionContentSerializer, SectionContentCreateSerializer, PageMetaSerializer
from utils.permissions import IsAdminOrReadOnly
from utils.mixins import CacheResponseMixin
# Create your views here.

class PageMetaViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PageMetaSerializer
    queryset = PageMeta.objects.all()
    filterset_fields = ['page_id']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_root'] = True
        return context

class PageCreateView(CreateAPIView):
    queryset = Section.objects.filter(page__isnull=True).select_related("page_meta")
    serializer_class = PageSerializer
    permission_classes = (IsAdminOrReadOnly,)
    

class PageGetViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    queryset = Section.objects.filter(page__isnull=True)\
        .prefetch_related(*Section.PREFETCH_FIELDS, Prefetch(
            lookup="page_section_set", 
            queryset=Section.objects.prefetch_related(*Section.PREFETCH_FIELDS))
        )
    serializer_class = PageSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class DestrySection(DestroyAPIView):
    queryset = Section.objects.exclude(is_default=True)
    permission_classes = (IsAdminOrReadOnly,)


class SectionContentView(CacheResponseMixin, ModelViewSet):
    queryset = SectionContent.objects.all()
    serializer_class = SectionContentSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "create":
            return SectionContentCreateSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':                
            context['add_to_field'] = self.validate_add_to_field(self.request.GET.get('add_to_field', 'content'))
        return context
    
    def validate_add_to_field(self, value):
        if value in ['content', 'description']:
            return value
        raise ValidationError(code="invalid_choice")


class TitleViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_context(self):
        data = super().get_serializer_context()
        data['is_root'] = True
        return data