from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def inbox_view(request):
    user = request.user

    # ✅ Top-level messages only (not replies)
    top_messages = Message.objects.filter(receiver=user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies', 'replies__sender', 'replies__receiver')

    return render(request, 'messaging/inbox.html', {'messages': top_messages})


