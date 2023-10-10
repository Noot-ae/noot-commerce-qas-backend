from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('token=<str:token>', ChatConsumer.as_asgi()),
]