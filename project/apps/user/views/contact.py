from rest_framework.generics import CreateAPIView
from ..serializers import ContactSerializer


class ContactCreateView(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = ()
    authentication_classes = ()    