from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from .serializers import PostSerializer, SubscriptionSerializer
from .models import Post, Subscription
from .filters import PostFilterSet
from utils.permissions import IsAdminOrReadOnly
# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().prefetch_related('title', 'body')
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PostFilterSet
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    

class SubscriptionCreateView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = ()
    authentication_classes = ()
    