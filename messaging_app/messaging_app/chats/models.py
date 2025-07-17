from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Extend the default Django User model
class CustomUser(AbstractUser):
    # Add any extra fields here if needed (e.g., profile_picture, bio)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username


# Conversation model that tracks participants
class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_usernames = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation between {participant_usernames}"


# Message model within a conversation
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp}"

