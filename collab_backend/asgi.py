import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.collaboration.routing import websocket_urlpatterns
from apps.collaboration.jwt_middleware import JWTAuthMiddleware # Import your middleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collab_backend.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(  # Wrap the URLRouter with your JWT Middleware
        URLRouter(websocket_urlpatterns)
    ),
})