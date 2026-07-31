from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from restaurants.users.models import Conversation, Message


class ClientMessagesView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard/user_dashboad/messages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create conversation for the logged in user
        conversation, created = Conversation.objects.get_or_create(user=self.request.user)
        context['conversation'] = conversation
        
        # Fetch messages
        chat_messages = conversation.messages.select_related('sender').order_by('created')
        context['chat_messages'] = chat_messages
        
        # Mark admin messages as read
        unread_admin_messages = chat_messages.filter(is_read=False).exclude(sender=self.request.user)
        if unread_admin_messages.exists():
            unread_admin_messages.update(is_read=True, read_at=timezone.now())
            
        # Fetch user's recent orders to display in the select dropdown
        if hasattr(self.request.user, 'client_profile'):
            context['recent_orders'] = self.request.user.client_profile.orders.order_by('-created')[:10]
        else:
            context['recent_orders'] = []
            
        return context

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content', '').strip()
        attachment = request.FILES.get('attachment')
        order_id = request.POST.get('order_id')
        
        if content or attachment:
            conversation, created = Conversation.objects.get_or_create(user=request.user)
            
            order = None
            if order_id and hasattr(request.user, 'client_profile'):
                from restaurants.meal.models import Order
                order = Order.objects.filter(id=order_id, client=request.user.client_profile).first()
                
            # Create message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                order=order,
                content=content,
                attachment=attachment,
                is_read=False
            )
            
            # Update last message time
            conversation.last_message_at = timezone.now()
            conversation.save()
            
            messages.success(request, "Message envoyé.")
            return redirect("users:client-messages")
            
        messages.error(request, "Impossible d'envoyer le message. Le contenu est vide.")
        return redirect("users:client-messages")
