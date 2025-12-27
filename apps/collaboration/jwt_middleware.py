from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(token):
    try:
        # 🔥 ALL Django imports must be LAZY
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.tokens import AccessToken

        if not token:
            return AnonymousUser()

        User = get_user_model()
        access = AccessToken(token)
        return User.objects.get(id=access["user_id"])

    except Exception:
        from django.contrib.auth.models import AnonymousUser
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope["query_string"].decode())
        token = query.get("token", [None])[0]

        scope["user"] = await get_user(token)
        return await super().__call__(scope, receive, send)
