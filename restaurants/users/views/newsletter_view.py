import json
from django.http import JsonResponse
from django.views import View
from restaurants.users.models import NewsletterSubscriber

class NewsletterSubscribeView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()

            if not email:
                return JsonResponse({"status": "error", "message": "L'adresse email est requise."}, status=400)

            # Check if exists (including soft-deleted ones if we want to restore, but let's just use all_objects or simple exists)
            # If the user unsubscribed (soft-deleted), we might want to restore them.
            subscriber = NewsletterSubscriber.all_objects.filter(email=email).first()
            
            if subscriber:
                if subscriber.is_deleted:
                    subscriber.restore()
                    return JsonResponse({"status": "success", "message": "Bon retour ! Vous êtes à nouveau abonné à notre newsletter."})
                else:
                    return JsonResponse({"status": "error", "message": "Cette adresse email est déjà abonnée."}, status=400)

            NewsletterSubscriber.objects.create(email=email)
            return JsonResponse({"status": "success", "message": "Merci pour votre inscription à notre newsletter !"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Requête invalide."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": "Une erreur est survenue."}, status=500)
