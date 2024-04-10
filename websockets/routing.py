from django.urls import path

from . import consumers


ws_urlpatterns = [
    path('ws/speed-data/', consumers.Consumer.as_asgi()),
]