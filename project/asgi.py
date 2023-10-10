import logging

logger = logging.getLogger('daphne')

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

from .middleware import TokenAuthMiddleware
from .apps.chat.websockets.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    )
})