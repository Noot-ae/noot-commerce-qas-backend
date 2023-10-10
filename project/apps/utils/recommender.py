from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE, related_name="user_event_set")
    product = models.ForeignKey('product.Product', models.CASCADE, related_name="product_event_set")
    created_at = models.DateTimeField(auto_now_add=True)

    class EventType(models.IntegerChoices):
        seen = 1, "Visited the product page"
        searched = 2, "User searched for the product"
        cart = 3, "Added to cart"
        bought = 4, "User purchased the product"

    event_type = models.IntegerField(choices=EventType.choices)

class Recommendation(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE, related_name="user_recommended_set")
    product = models.ForeignKey('product.Product', models.CASCADE, related_name="product_recommended_set")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'interaction_type')

def calculate_similarity(user1, user2):
    user1_events = set(user1.user_event_list.values_list('product_id', flat=True))
    user2_events = set(user2.user_event_list.values_list('product_id', flat=True))

    intersection = user1_events & user2_events
    union = user1_events | user2_events

    #similarity = len(intersection) / len(union) if len(union) > 0 else 0
    weight = intersection.aggregate(weight=models.Sum('event_type'))

    #return by event priority  
    return weight


def get_similar_users(user, limit=5):
    all_users = User.objects.exclude(id=user.id).prefetch_related('user_event_set')
    similarities = [(other_user, calculate_similarity(user, other_user)) for other_user in all_users]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [user_similarity[0] for user_similarity in similarities[:limit]]


def recommend_products(user, limit=5):
    similar_users = get_similar_users(user, limit)
    already_recommended_product = set(Recommendation.objects.filter(user=user).values_list('product_id', flat=True))
    to_be_recommended_products = set()

    for similar_user in similar_users:
        events = Event.objects.filter(user__in=similar_user).exclude(
            models.Q(
                models.Q(product_id__in=to_be_recommended_products) | models.Q(product_id__in=already_recommended_product)
            )
        )
        
        for event in events:
            to_be_recommended_products.add(event.product)

    return to_be_recommended_products


from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from product.serializers import ProductSerializer

class RecommendationSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        modle = Recommendation
        fields = '__all__'

class RecommendedProduct(ListAPIView):
    queryset = Recommendation.objects.all().select_related('product')
    serializer_class = RecommendationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs