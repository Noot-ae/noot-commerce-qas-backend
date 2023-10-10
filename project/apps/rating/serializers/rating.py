from rest_framework import serializers
from ..models import ProductRating, VenderRating, ProductReply
from vender.models import Vender
from django.contrib.auth import get_user_model
from user.serializers import CustomerDisplaySerializer
from product.models import Product

User = get_user_model()

class RatingBaseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = CustomerDisplaySerializer(instance.user).data
        return data
    
    
class VenderRatingSerializer(RatingBaseSerializer):
    vender = serializers.SlugRelatedField(slug_field="user__username", queryset=Vender.objects.all())
    
    class Meta:
        model = VenderRating
        fields = '__all__'


class ProductRatingSerializer(RatingBaseSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_ratable=True))

    class Meta:
        model = ProductRating
        fields = '__all__'


class ProductRateReplySerializer(RatingBaseSerializer):

    class Meta:
        model = ProductReply
        fields = '__all__'
        extra_kwargs = {
            "likes" : {"read_only" : True}
        }

