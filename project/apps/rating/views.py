from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .serializers import  VenderRatingSerializer, ProductRatingSerializer, ProductRateReplySerializer
from .models import ProductRating, VenderRating, ProductReply
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from typing import Union
from utils.decorators import get_queryset_wrapper


class BaseRatingViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @get_queryset_wrapper
    def get_queryset(self):
        if self.request.method in ['DELETE', 'PATCH', 'UPDATE']:
            user = self.request.user
            return super().get_queryset().filter(user=user)
        return super().get_queryset()

        
class ProductRatingViewSet(BaseRatingViewSet):
    queryset = ProductRating.objects.select_related('user').filter(product__is_ratable=True)
    serializer_class = ProductRatingSerializer
    filterset_fields = ['product', 'user']


class VenderRatingViewSet(BaseRatingViewSet):
    queryset = VenderRating.objects.select_related('user')
    serializer_class = VenderRatingSerializer
    filterset_fields = ['user', 'vender']


class ProductReplyViewSet(ModelViewSet):
    queryset = ProductReply.objects.all()
    serializer_class = ProductRateReplySerializer
    filterset_fields = ['parent_comment', 'parent_reply']
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            return qs
        return qs.filter(user=self.request.user)


class LikeViewSet(APIView):
    models = {
        "product_reply" : ProductReply,
        "product_rate" : ProductRating,
        "vender_rate" : VenderRating 
    }
    
    def get_model(self, model_name):
        try:
            Model = self.models[model_name]
        except KeyError:
            raise ValidationError(f"wrong model choice, choices are: {self.models.keys()}")
        return Model

    
    def post(self, request, model_name, pk, action):
        
        Model = self.get_model(model_name)
            
        object : Union[ProductReply, ProductRating, VenderRating] = get_object_or_404(Model, pk=pk)
        
        if action == "add":                
            object.likes.add(request.user)
        else:
            object.likes.remove(request.user)
        
        object.save()
        return Response("success")
    
    
    
    
        