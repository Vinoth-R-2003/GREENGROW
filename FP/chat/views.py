from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from users.models import User

@login_required
def conversations(request):
    # Get all users who have exchanged messages with the current user
    # This is a basic implementation; for production, use distinct() on database properly
    sent = Message.objects.filter(sender=request.user).values_list('recipient', flat=True)
    received = Message.objects.filter(recipient=request.user).values_list('sender', flat=True)
    
    # Combine sets of user IDs
    contact_ids = set(list(sent) + list(received))
    contacts = User.objects.filter(id__in=contact_ids)
    
    return render(request, 'chat/conversations.html', {'contacts': contacts})

@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Get messages between these two users (ordered by timestamp)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')
    
    # Get call logs between these two users
    from .models import CallLog
    call_logs = CallLog.objects.filter(
        (Q(caller=request.user) & Q(receiver=other_user)) |
        (Q(caller=other_user) & Q(receiver=request.user))
    ).order_by('-started_at')[:10]  # Last 10 calls
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                content=content
            )
            return redirect('chat_room', user_id=user_id)
            
    return render(request, 'chat/room.html', {
        'other_user': other_user,
        'messages': messages,
        'call_logs': call_logs
    })

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender:
        recipient = message.recipient
        message.delete()
        return redirect('chat_room', user_id=recipient.id)
    return redirect('conversations')
