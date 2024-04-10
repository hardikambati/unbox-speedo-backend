import json
from asgiref.sync import sync_to_async

# 3rd party
from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    """
    Base class for connection, disconnection and sending messages to 
    websocket consumers
    """

    async def connect(self):
        """
        Connect users to rooms
        """
        print(f'[websocket] connected : {self.channel_name}')
        
        await self.accept()

        # add client to room [room name = 'sensor']
        await self.channel_layer.group_add(
            'sensor',
            self.channel_name
        )


    async def disconnect(self, close_code):
        """
        Remove users to rooms
        """
        print(f'[websocket] disconnected : {self.channel_name}')

        await self.channel_layer.group_discard(
            'sensor',
            self.channel_name
        )


    async def speed_update(self, event):
        """
        Send sensor speed data to room [room name = 'sensor']
        """

        message = event['message']
        
        print(f'[websocket] {message}')

        str_message = json.dumps(message)
        await self.send(text_data=str_message)
