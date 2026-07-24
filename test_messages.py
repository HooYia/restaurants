from django.contrib.auth import get_user_model
from restaurants.users.models import Conversation, Message
from restaurants.meal.models import Client

User = get_user_model()
client_user = User.objects.filter(is_staff=False).first()

if client_user:
    conv, created = Conversation.objects.get_or_create(user=client_user)
    Message.objects.create(conversation=conv, sender=client_user, content="Bonjour, je voudrais savoir si vous livrez le dimanche ?", is_read=False)
    import datetime
    from django.utils import timezone
    conv.last_message_at = timezone.now()
    conv.save()
    print("Test conversation created for", client_user.email)
else:
    print("No client user found.")
