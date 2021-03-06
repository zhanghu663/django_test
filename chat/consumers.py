import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        a = 1
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        print("room_name:{}, room_group_name:{}".format(self.room_name, self.room_group_name))

    def disconnect(self, close_code):
        print("group discard")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # 此方法为接受前端发送过来的数据
        text_data_json = json.loads(text_data)
        print("text_data_json:{}, Send message to room group".format(text_data_json))
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        # 此方法为向前端发送数据
        print("send message to websocket")
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
