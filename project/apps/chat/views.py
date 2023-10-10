from .filters import ChatFilter
from utils.decorators import get_queryset_wrapper
from .models import Message
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView
from .serializers import MessageSerializer, ChatListSerializer
from django.db.models import Q, OuterRef, Subquery, Exists
from django.contrib.auth import get_user_model

User = get_user_model()

latest_message = Message.objects.filter(
    Q(sender=OuterRef('pk')) | Q(receiver=OuterRef('pk'))
).order_by('-created_at').values('created_at', 'message')[:1]

# Create your views here.
class ChatViewSet(DestroyModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_class = ChatFilter

    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method == "DELETE":                
            return qs.filter(
                Q(
                    Q(sender=self.request.user) | Q(receiver=self.request.user)
                )
            )
        return qs
    

class ListPreviousChatViewSet(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ChatListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.user
        
        qs = qs.exclude().filter(
            Exists(
                Subquery(
                    Message.objects.filter(
                        Q(sender_id=OuterRef('pk'), receiver_id=user_id) | Q(receiver_id=OuterRef('pk'), sender_id=user_id)
                    )
                )
            )
        ).distinct()

        qs = qs.annotate(
            last_message_date=Subquery(latest_message.values('created_at')),
            last_message_text=Subquery(latest_message.values('message')),
        )
        return qs
