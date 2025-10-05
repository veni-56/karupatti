from .models import Conversation, Message


def unread_messages_count(request):
    """Add unread messages count to all templates"""
    if request.user.is_authenticated:
        try:
            # Get all conversations where user is either buyer or seller
            conversations = Conversation.objects.filter(
                models.Q(buyer=request.user) | models.Q(seller=request.user)
            )
            
            # Count unread messages across all conversations
            unread_count = 0
            for conversation in conversations:
                unread_count += conversation.unread_count(request.user)
            
            return {'unread_messages_count': unread_count}
        except Exception:
            return {'unread_messages_count': 0}
    return {'unread_messages_count': 0}
