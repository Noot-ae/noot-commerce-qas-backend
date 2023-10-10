import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        schema_name = self.scope['schema_name']
        # Join room
        self.room_group_name = f"{schema_name}_user_{self.user.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from websocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        data['type'] ='chat_message'
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            data
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))