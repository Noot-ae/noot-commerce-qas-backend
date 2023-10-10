from rest_framework.viewsets import ReadOnlyModelViewSet
from user.permissions import IsVender
from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer
from django.db.models import Prefetch, Exists, OuterRef
from .models import Vender
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import VenderRegisterSerializer
from rest_framework.permissions import IsAdminUser
from user.serializers import UserListSerializer
from utils.decorators import get_queryset_wrapper

# Create your views here.
User = get_user_model()

class VenderOrdersViewset(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsVender,)

    @get_queryset_wrapper
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            Exists(
                OrderProduct.objects.filter(product_variant__product__user=self.request.user)
            )
        ).prefetch_related(
            Prefetch(
                'order_item_set', 
                queryset=OrderProduct.objects.filter(product_variant__product__user=self.request.user)
            )
        )
        return queryset
    

class VenderListViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.filter(Exists(Vender.objects.filter(user_id = OuterRef('pk'))))
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)


class VenderRegisterView(CreateAPIView):
    serializer_class = VenderRegisterSerializer
    queryset = User.objects.all()
    permission_classes = ()
    