from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from ..serializers import PromoteUserPermissionSerializer, ActivateUserSerializer
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..filters import UserMailFilter
from ..permissions import IsSuperuser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view
from ..models import User, OTP
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from ..serializers import VerifyOtpUsernameSerializer


class PromoteUserPermissionView(ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PromoteUserPermissionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserMailFilter
    permission_classes = (IsSuperuser,)
    filterset_fields = ['email']


@api_view(['GET'])
def is_logged_in(request):
    return Response({'username' : request.user.username}, status=HTTP_200_OK)


class ActivateUserView(APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def validate_serializer(self):
        serializer = ActivateUserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data        
    
    def post(self, request):
        otp : OTP = self.validate_serializer()['otp']
        user : User = otp.user
        user.activate()
        otp.delete()
        return Response()


class OtpUsernameView(CreateAPIView):
    serializer_class = VerifyOtpUsernameSerializer
    queryset = User.objects.all()    
    permission_classes = ()
    authentication_classes = ()