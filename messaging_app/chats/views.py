from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import status


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show only conversations the current user is part of
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)  # Add the creator
        # Optionally allow adding other participants via request data
        other_user_ids = self.request.data.get("participants", [])
        for user_id in other_user_ids:
            try:
                user = User.objects.get(user_id=user_id)
                conversation.participants.add(user)
            except User.DoesNotExist:
                continue


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show messages only for conversations the user is part of
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise PermissionError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

