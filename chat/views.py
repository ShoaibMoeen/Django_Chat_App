from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from chat.models import Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.models import User
from chat.models import Room
from django.views.generic.edit import View
from django.db.models import Q
import json
from django.http import JsonResponse
from datetime import datetime,timedelta
import pytz


@login_required
def index(request):

    chats = Room.objects.filter(Q(user_1 = request.user) | Q(user_2 = request.user))
    users = User.objects.values('username').filter(~Q(username=request.user.username))
    for chat in chats:
        other_user = chat.other_user(request.user)
        chat.other_user = other_user.username
    date_min = datetime(1980, 8, 15, 8, 15, 12, 0, pytz.UTC)
    chat_sorted = sorted(chats, key=lambda t: t.last_msg.timestamp if t.last_msg else date_min, reverse=True)
    return render(request, 'chat/index.html',{'chats':chat_sorted, 'users':users})


@login_required
def room(request, room_name):

    room = Room.objects.get(room_name = room_name)

    if room:
        if str(request.user) == str(room.user_1) or str(request.user) == str(room.user_2):
            msg = Message.objects.filter(room=room).order_by('timestamp')
            chats = Room.objects.filter(Q(user_1=request.user) | Q(user_2=request.user))
            for chat in chats:
                other_user = chat.other_user(request.user)
                chat.other_user = other_user.username
            other = room.other_user(request.user)
            date_min = datetime(1980, 8, 15, 8, 15, 12, 0, pytz.UTC)
            chat_sorted = sorted(chats, key=lambda t: t.last_msg.timestamp if t.last_msg else date_min, reverse=True)
            users = User.objects.values('username').filter(~Q(username=request.user.username))
            return render(request, 'chat/room.html', {
                'room_name': room_name ,'messages':msg, 'chats':chat_sorted, 'other_user': other, 'users':users
            })
    return HttpResponseRedirect(reverse('chat:index'))


@method_decorator(login_required(), name='dispatch')
class Get_Room(View):

    def post(self, request):
        user_1 = self.request.user
        user_name = json.loads(request.POST.get("user_2"))
        user_2 = User.objects.get(username = user_name)
        rooms = Room.objects.filter(user_1=user_1, user_2=user_2)
        if not rooms:
            rooms = Room.objects.filter(user_1=user_2,user_2=user_1)

        if not rooms:
            room = Room(user_1=user_1,user_2=user_2)
            room.save()
        else:
            room = rooms[0]

        return JsonResponse({"room_name": room.room_name})


def Rediect(request):
    return HttpResponseRedirect(reverse('chat:index'))
