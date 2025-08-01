from .models import Message

def get_conversation(conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id, parent_message__isnull=True)\
        .select_related('sender')\
        .prefetch_related('replies__sender')
    return messages

