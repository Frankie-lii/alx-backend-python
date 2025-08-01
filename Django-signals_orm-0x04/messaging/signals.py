from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender  # or any user with edit rights
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


