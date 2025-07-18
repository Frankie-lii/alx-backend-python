from rest_framework import serializers
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at']

