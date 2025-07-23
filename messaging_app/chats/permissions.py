from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Conversation-based permissions
        # For Conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Messages (check the related conversation)
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

