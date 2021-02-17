import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message,Room
from users.models import User
from datetime import datetime, timezone
from django.core.serializers import serialize
import pytz

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        room_name = self.scope['url_route']['kwargs']['room_name']
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_name = text_data_json['sender']
        room = Room.objects.get(room_name=room_name)
        sender_user = User.objects.get(username=sender_name)
        msg = Message(room=room,sender=sender_user,message=message,timestamp=datetime.utcnow())
        msg_date = msg.timestamp.strftime("%b. %d, %Y")
        msg_time = msg.timestamp.strftime("%I:%M ")
        message_p = msg.timestamp.strftime("%p")
        timezone = pytz.timezone("UTC")
        with_timezone = timezone.localize(msg.timestamp)
        msg.timestamp = with_timezone
        msg_time_millis=msg.convert

        message_period = '.'.join([x.lower() for x in message_p if x=='A' or x=='M' or x=='P'])
        msg_time += message_period+'.'
        message_time = {'date':msg_date,'time':msg_time,'hour':msg.timestamp.hour, 'minutes':msg.timestamp.minute,'time_millis': msg_time_millis, 'inbox_time':msg_date}
        today_date = datetime.now()
        if msg.timestamp.date() == today_date.date():
            message_time['inbox_time'] = msg_time
        msg.save()
        sender_id = str(sender_user.key)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_id,
                'message_time': message_time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        message_time = event['message_time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender':sender,
            'message_time': message_time
        }))