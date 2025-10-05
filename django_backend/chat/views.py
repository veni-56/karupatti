from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, Max
from .models import Conversation, Message
from store.models import Shop, Product


@login_required
def conversation_list(request):
    """List all conversations for the user"""
    # Get conversations where user is buyer or seller
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user),
        is_active=True
    ).select_related('buyer', 'seller', 'shop', 'product').prefetch_related('messages')
    
    # Add unread count to each conversation
    for conv in conversations:
        conv.unread = conv.unread_count(request.user)
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'chat/conversation_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """View a specific conversation"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        is_active=True
    )
    
    # Check if user is part of this conversation
    if request.user not in [conversation.buyer, conversation.seller]:
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('chat:conversation_list')
    
    # Mark messages as read
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True, read_at=timezone.now())
    
    # Get messages
    chat_messages = conversation.messages.all().select_related('sender')
    
    # Determine other user
    other_user = conversation.seller if request.user == conversation.buyer else conversation.buyer
    
    context = {
        'conversation': conversation,
        'messages': chat_messages,
        'other_user': other_user,
    }
    return render(request, 'chat/conversation_detail.html', context)


@login_required
def send_message(request, conversation_id):
    """Send a message in a conversation"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is part of this conversation
    if request.user not in [conversation.buyer, conversation.seller]:
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    message_text = request.POST.get('message', '').strip()
    image = request.FILES.get('image')
    
    if not message_text and not image:
        return JsonResponse({'success': False, 'message': 'Message cannot be empty'})
    
    # Create message
    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        message=message_text,
        image=image
    )
    
    # Update conversation timestamp
    conversation.updated_at = timezone.now()
    conversation.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Message sent',
        'data': {
            'id': message.id,
            'sender': message.sender.username,
            'message': message.message,
            'image': message.image.url if message.image else None,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })


@login_required
def start_conversation(request, shop_id):
    """Start a new conversation with a shop"""
    shop = get_object_or_404(Shop, id=shop_id, is_active=True)
    
    if request.user == shop.owner:
        messages.error(request, 'You cannot chat with your own shop.')
        return redirect('store:shop_detail', slug=shop.slug)
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        buyer=request.user,
        seller=shop.owner,
        shop=shop
    )
    
    # If product_id is provided, associate it
    product_id = request.GET.get('product_id')
    if product_id and not conversation.product:
        try:
            product = Product.objects.get(id=product_id, shop=shop)
            conversation.product = product
            conversation.save()
        except Product.DoesNotExist:
            pass
    
    return redirect('chat:conversation_detail', conversation_id=conversation.id)


@login_required
def delete_conversation(request, conversation_id):
    """Delete/archive a conversation"""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Check if user is part of this conversation
        if request.user in [conversation.buyer, conversation.seller]:
            conversation.is_active = False
            conversation.save()
            messages.success(request, 'Conversation deleted.')
        else:
            messages.error(request, 'Access denied.')
    
    return redirect('chat:conversation_list')


@login_required
def get_unread_count(request):
    """Get total unread message count for user"""
    unread_count = Message.objects.filter(
        Q(conversation__buyer=request.user) | Q(conversation__seller=request.user),
        is_read=False
    ).exclude(sender=request.user).count()
    
    return JsonResponse({'unread_count': unread_count})
