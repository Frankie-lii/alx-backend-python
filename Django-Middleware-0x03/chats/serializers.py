from rest_framework import serializers
from .models import User, Conversation, Message
from django.core.exceptions import ValidationError


# ✅ 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']


# ✅ 2. Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_email', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sender_email', 'sent_at']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


# ✅ 3. Conversation Serializer (with nested messages)
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.order_by('-sent_at')[:10]  # limit to latest 10
        return MessageSerializer(messages, many=True).data

