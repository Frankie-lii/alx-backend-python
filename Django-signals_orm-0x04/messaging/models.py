from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Track if message has been read

    # Existing fields for threading, editing, etc.
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    edited = models.BooleanField(default=False)

    # Use the custom manager
    objects = models.Manager()  # Default manager
    unread_messages = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:30]}"

