from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import User, Testimonial


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.AdminUserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


from django import forms

class UserProfileUpdateForm(forms.ModelForm):
    """
    Formulaire pour la mise à jour des informations de profil.
    L'email est en lecture seule.
    """
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
        self.fields["email"].help_text = "Votre adresse e-mail ne peut pas être modifiée."
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["phone"].required = True


class TestimonialForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "maxlength": "300",
            "placeholder": "Partagez votre expérience avec nous... (300 caractères max)"
        }),
        label="Votre avis"
    )

    class Meta:
        model = Testimonial
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
                "max": "5",
                "id": "rating-input",
                "style": "display: none;" # We will use a custom star widget UI
            }),
        }
        labels = {
            "rating": "Note",
        }

