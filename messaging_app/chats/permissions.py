from rest_framework import permissions

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

