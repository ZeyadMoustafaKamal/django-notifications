from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = 'notifications_{}'.format(self.user.id)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, code):
        await self.close()
    
    async def notify(self, event):
        title      = event['title']
        content    = event['content']
        created_at = event['created_at']

        text_data = json.dumps({
            'title': title,
            'content': content,
            'created_at':created_at
        })
        await self.send(text_data=text_data)

