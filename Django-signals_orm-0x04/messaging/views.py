from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

@login_required
def unread_inbox_view(request):
    unread_messages = (
        Message.objects
        .filter(receiver=request.user, read=False)
        .only('id', 'sender__username', 'content', 'timestamp')
        .select_related('sender')
    )
    return render(request, 'messaging/unread_inbox.html', {
        'messages': unread_messages
    })

