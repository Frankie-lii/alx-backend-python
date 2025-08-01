from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm

@login_required
def inbox_view(request):
    # Get all top-level messages received by the user
    messages = Message.objects.filter(
        receiver=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies', 'replies__sender', 'replies__receiver')

    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def sent_messages_view(request):
    # Get all messages sent by the user
    messages = Message.objects.filter(
        sender=request.user
    ).select_related('receiver', 'sender').prefetch_related('replies')

    return render(request, 'messaging/sent.html', {'messages': messages})


@login_required
def message_detail_view(request, message_id):
    # View a specific message and its replies
    message = get_object_or_404(Message, id=message_id)

    if message.receiver != request.user and message.sender != request.user:
        return redirect('inbox')  # Prevent access to others' messages

    replies = message.replies.select_related('sender', 'receiver').prefetch_related('replies')

    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'replies': replies
    })


@login_required
def send_message_view(request, receiver_id=None, parent_id=None):
    receiver = None
    parent_message = None

    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)
    if parent_id:
        parent_message = get_object_or_404(Message, id=parent_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver or parent_message.receiver
            message.parent_message = parent_message
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {
        'form': form,
        'receiver': receiver,
        'parent_message': parent_message
    })

