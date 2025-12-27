from django.urls import re_path
from .consumers import WorkspaceConsumer

websocket_urlpatterns = [
    re_path(r"^ws/workspaces/(?P<workspace_id>\d+)/$", WorkspaceConsumer.as_asgi()),
]
