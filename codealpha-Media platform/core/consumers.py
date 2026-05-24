import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LiveStreamConsumer(AsyncWebsocketConsumer):
    """
    WebRTC Signaling server for live streams.
    Each stream room is identified by stream_id.
    """

    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.room_group_name = f'stream_{self.stream_id}'

        # Join stream room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Notify others the stream ended / viewer left
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'stream_signal', 'data': {'type': 'peer-disconnected'}}
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Relay signaling messages (offer, answer, ICE candidates) to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'stream_signal',
                'data': data,
                'sender_channel': self.channel_name,
            }
        )

    async def stream_signal(self, event):
        # Don't echo back to sender
        if event.get('sender_channel') == self.channel_name:
            return
        await self.send(text_data=json.dumps(event['data']))
