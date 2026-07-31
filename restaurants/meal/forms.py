from django import forms
from .models import Category, Meal, Accompaniment, DailyMenu, Boisson

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Nom de la catégorie'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ordre d\'affichage (ex: 1)'
            }),
        }
        labels = {
            'name': 'Nom',
            'display_order': 'Ordre d\'affichage'
        }


class MealForm(forms.ModelForm):
    daily_menus = forms.ModelMultipleChoiceField(
        queryset=DailyMenu.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-input'}),
        required=False,
        label='Jours du menu (Ctrl+clic pour plusieurs)'
    )

    class Meta:
        model = Meal
        fields = [
            'name', 'description', 'price', 'image', 'category',
            'accompaniments', 'max_included_accompaniments',
            'availability_mode', 'is_available'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'accompaniments': forms.SelectMultiple(attrs={'class': 'form-input'}),
            'max_included_accompaniments': forms.NumberInput(attrs={'class': 'form-input'}),
            'availability_mode': forms.Select(attrs={'class': 'form-input'}),
        }
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'price': 'Prix',
            'image': 'Photo',
            'category': 'Catégorie',
            'accompaniments': 'Accompagnements',
            'max_included_accompaniments': 'Accompagnements inclus',
            'availability_mode': 'Mode de disponibilité',
            'is_available': 'Disponible',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['daily_menus'].initial = self.instance.daily_menus.all()

    def save(self, commit=True):
        meal = super().save(commit=False)
        if commit:
            meal.save()
            self.save_m2m() # Saves accompaniments
            meal.daily_menus.set(self.cleaned_data['daily_menus'])
        return meal


class AccompanimentForm(forms.ModelForm):
    class Meta:
        model = Accompaniment
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Nom de l\'accompagnement'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input', 
                'step': '0.01',
                'placeholder': 'Prix (ex: 500)'
            }),
        }
        labels = {
            'name': 'Nom',
            'price': 'Prix (FCFA)'
        }


class BoissonForm(forms.ModelForm):
    class Meta:
        model = Boisson
        fields = ['name', 'price', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom de la boisson'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Prix (ex: 500)'}),
        }
        labels = {
            'name': 'Nom',
            'price': 'Prix (FCFA)',
            'image': 'Photo',
            'is_available': 'Disponible',
        }


class CustomOrderRequestForm(forms.ModelForm):
    class Meta:
        model = __import__('restaurants.meal.models', fromlist=['CustomOrderRequest']).CustomOrderRequest
        fields = ['description', 'quantity', 'target_date']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-input', 
                'rows': 4,
                'placeholder': 'Décrivez le plat que vous souhaitez, vos préférences, allergies...'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input', 
                'min': '1',
                'placeholder': 'Nombre de personnes'
            }),
            'target_date': forms.DateInput(attrs={
                'class': 'form-input', 
                'type': 'date'
            }),
        }
        labels = {
            'description': 'Description de votre demande',
            'quantity': 'Pour combien de personnes ?',
            'target_date': 'Date souhaitée (Optionnel)',
        }
