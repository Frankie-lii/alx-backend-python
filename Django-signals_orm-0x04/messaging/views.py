from django.contrib.auth.decorators import login_require
from django.shortcuts import render
from .models import Message

@login_required
def unread_inbox_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {
        'messages': unread_messages
    })

