from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Main router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router: messages under a specific conversation
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Export the URLs
urlpatterns = router.urls + conversation_router.urls

