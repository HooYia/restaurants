from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from restaurants.users.models import Conversation, Message
from restaurants.meal.views.admin_category_views import AdminRequiredMixin


class AdminMessagesView(AdminRequiredMixin, TemplateView):
    template_name = "pages/dashboard/admin_dashboard/messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all conversations, ordered by the latest activity
        conversations = Conversation.objects.select_related('user').order_by('-last_message_at')
        
        for conv in conversations:
            conv.unread_count = conv.messages.filter(is_read=False).exclude(sender__is_staff=True).count()
        
        context['conversations'] = conversations
        
        conversation_id = self.request.GET.get('conversation_id')
        if conversation_id:
            active_conversation = get_object_or_404(Conversation, id=conversation_id)
            context['active_conversation'] = active_conversation
            
            chat_messages = active_conversation.messages.select_related('sender').order_by('created')
            context['chat_messages'] = chat_messages
            
            unread_client_messages = chat_messages.filter(is_read=False).exclude(sender=self.request.user)
            if unread_client_messages.exists():
                unread_client_messages.update(is_read=True, read_at=timezone.now())
                
        return context

    def post(self, request, *args, **kwargs):
        conversation_id = request.POST.get('conversation_id')
        content = request.POST.get('content', '').strip()
        attachment = request.FILES.get('attachment')
        
        if conversation_id and (content or attachment):
            conversation = get_object_or_404(Conversation, id=conversation_id)
            
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
                attachment=attachment,
                is_read=False
            )
            
            conversation.last_message_at = timezone.now()
            conversation.save()
            
            messages.success(request, "Message envoyé.")
            return redirect(f"{request.path}?conversation_id={conversation.id}")
            
        messages.error(request, "Impossible d'envoyer le message. Le contenu est vide.")
        if conversation_id:
            return redirect(f"{request.path}?conversation_id={conversation_id}")
        return redirect(request.path)
