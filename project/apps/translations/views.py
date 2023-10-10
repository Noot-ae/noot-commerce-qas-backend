from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from googletrans import Translator
from .serializers import TranslateSerializer, TranslationSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Translation
from .permissions import TranslationPermission
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from product.models import Product
from django.db.models import Q, Exists, Subquery
from product.serializers import ProductSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class TranslateView(APIView):

    def post(self, request):
        serializer = TranslateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        translated_text = self.translate(data)
        return Response({'translated_text' : translated_text.text})

    def translate(self, data : dict):
        translator = Translator()
        try:                
            translated_text = translator.translate(data['text'], data['destination'])
        except ValueError as e:
            raise ValidationError("destination is invalid")
        
        return translated_text


class TranslationUpdateView(DestroyModelMixin, UpdateModelMixin, ReadOnlyModelViewSet):
    SENSITIVE_METHODS = ['PUT', 'PATCH', 'DELETE']

    serializer_class = ProductSerializer
    queryset = Product.objects.all().prefetch_related('description', 'productvarient_set__name')
    permission_classes = (TranslationPermission,)


    def get_object(self):
        if self.request.method in self.SENSITIVE_METHODS:
            return self.get_translation()
        return super().get_object()
    
    def get_translation(self):
        self.serializer_class = TranslationSerializer
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        translation_id = self.kwargs['translation_id']

        parent_product_subquery = Exists(Subquery(Product.objects.filter(
            Q(
                Q(description__id__in=[translation_id]) | Q(name__id__in=[translation_id])
            ),is_online=True,
            user=self.request.user,                                    
            **filter_kwargs,            
            ).only('pk')))

        obj = get_object_or_404(
            Translation.objects.annotate(
                is_user_owner=parent_product_subquery
            ), 
            pk=translation_id
        )
        
        self.check_object_permissions(self.request, obj)
        return obj
