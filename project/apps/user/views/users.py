from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from ..serializers import UserListSerializer, UserProfileSerializer, UserUpdateSerializer, EmailChangeSerializer, SendEmailVerifyOTPSerializer, SendUserEmailVerifyOTPSerializer
from rest_framework.permissions import IsAdminUser
from django.db.models import Exists, OuterRef
from rest_framework.mixins import UpdateModelMixin
from vender.models import Vender
from ..auth import ProfileAuth
from rest_framework.generics import UpdateAPIView, CreateAPIView
from ..models import User
from ..filters import UserListFilter


class UserListViewSet(UpdateModelMixin, ReadOnlyModelViewSet):
    queryset = User.objects.filter(~Exists(Vender.objects.filter(user_id=OuterRef('pk'))))
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    filterset_class = UserListFilter


class BaseUserUpdateMixin:    
    def get_object(self):
        return self.request.user


class UserProfileViewSet(BaseUserUpdateMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    authentication_classes = (ProfileAuth,)
    
    
class UserUpdateView(BaseUserUpdateMixin, UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    

class UserEmailChangeView(BaseUserUpdateMixin, UpdateAPIView):
    serializer_class = EmailChangeSerializer
    queryset = User.objects.all()

    
class UserEmailVerifyView(BaseUserUpdateMixin, CreateAPIView):
    serializer_class = SendUserEmailVerifyOTPSerializer
    queryset = User.objects.all()

    def get_authenticators(self):
        if self.is_new:
            return []
        return super().get_authenticators()
    
    def get_permissions(self):
        if self.is_new:
            return []        
        return super().get_permissions()

    @property
    def is_new(self):
        return "is_new" in self.request.GET
    
    def get_serializer_class(self):
        if self.is_new:
            return SendEmailVerifyOTPSerializer
        return super().get_serializer_class()

