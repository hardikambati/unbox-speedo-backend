"""
ASGI config for speedometer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speedometer.settings')

application = get_asgi_application()

from websockets import routing


application = ProtocolTypeRouter({
    'http': application,
    'websocket': AuthMiddlewareStack(URLRouter(routing.ws_urlpatterns)),
})