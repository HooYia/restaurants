import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View

from restaurants.users.models import Client

User = get_user_model()


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:home")

class RegisterView(View):

    template_name = "users/register.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:

            messages.error(
                request,
                "Les mots de passe ne correspondent pas."
            )

            return redirect("/")

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Cette adresse email est déjà utilisée."
            )

            return redirect("/")

        if not phone:

            messages.error(
                request,
                "Le numéro de téléphone est obligatoire."
            )

            return redirect("/")

        if User.objects.filter(phone=phone).exists():

            messages.error(
                request,
                "Ce numéro de téléphone existe déjà."
            )

            return redirect("/")

        otp = random.randint(100000, 999999)

        request.session["otp"] = str(otp)

        request.session["register_data"] = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "password": password,
        }

        send_mail(
            subject="Code de vérification",
            message=f"Votre code OTP est : {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Un code de vérification a été envoyé à votre adresse email."
        )

        return redirect("users:verify-otp")


class VerifyOtpView(View):

    template_name = "users/verify_otp.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        print("JE SUIS DANS VERIFY OTP")
        otp = request.POST.get("otp", "").strip()

        

        session_otp = request.session.get("otp")
        register_data = request.session.get("register_data")

        if not session_otp or not register_data:

            messages.error(
                request,
                "Session expirée. Veuillez recommencer."
            )

            return redirect("/")

        if otp != session_otp:

            messages.error(
                request,
                "Code OTP invalide."
            )

            return redirect("users:verify-otp")

        user = User.objects.create_user(
            email=register_data["email"],
            phone=register_data["phone"],
            password=register_data["password"],
            first_name=register_data["first_name"],
            last_name=register_data["last_name"],
        )

        Client.objects.create(
            user=user
        )

        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend"
        )

       
        request.session.pop("otp", None)
        request.session.pop("register_data", None)


        messages.success(
            request,
            "Votre compte client a été créé avec succès."
        )


        print("MESSAGES AJOUTES")


        return redirect("users:client-dashboard"
        )