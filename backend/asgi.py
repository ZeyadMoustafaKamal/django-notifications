import os
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http':django_application,
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack((URLRouter(websocket_urlpatterns)))
    )
})