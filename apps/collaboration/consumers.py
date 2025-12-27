import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WorkspaceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("🔥 WS CONNECT ATTEMPT")
        print("PATH:", self.scope.get("path"))
        print("USER:", self.scope.get("user"))

        if self.scope["user"].is_anonymous:
            print("❌ ANONYMOUS — CLOSING")
            await self.close()
            return

        self.workspace_id = self.scope["url_route"]["kwargs"]["workspace_id"]
        self.group_name = f"workspace_{self.workspace_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        user = self.scope["user"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast",
                "event": "user_leave",
                "user": user.email,
            },
        )

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast",
                "event": data.get("event"),
                "payload": data.get("payload", {}),
                "user": self.scope["user"].email,
            },
        )

    async def broadcast(self, event):
        await self.send(text_data=json.dumps(event))
