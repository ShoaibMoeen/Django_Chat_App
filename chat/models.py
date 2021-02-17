from django.db import models
from datetime import datetime
from users.models import User
# Create your models here.
import uuid


def generate_uuid():
    return uuid.uuid4().hex

class Room(models.Model):

    room_name = models.CharField(max_length=40, default=generate_uuid, editable=False, unique=True)
    user_1 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=False, related_name="user_1"
    )
    user_2 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=False, related_name="user_2"
    )
    @property
    def last_msg(self):
        return Message.objects.filter(room=self.id).last()

    def other_user(self,curr_user):
        if self.user_1 ==curr_user:
            return self.user_2
        else:
            return self.user_1


class Message(models.Model):

    room = models.ForeignKey(
        "chat.Room", on_delete=models.CASCADE, null=False, related_name="room"
    )
    sender = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, related_name="sender"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def is_today(self):
        today =datetime.now()
        if self.timestamp.date() == today.date():
            return True
        return False

    @property
    def convert(self):
        return self.timestamp.timestamp()*1000
