from django import forms
from .models import Category, Meal

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
