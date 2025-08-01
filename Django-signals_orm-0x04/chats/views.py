from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from .models import Conversation, Message

@cache_page(60)
def conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).select_related('sender')
    return render(request, 'chats/conversation_messages.html', {
        'conversation': conversation,
        'messages': messages
    })

