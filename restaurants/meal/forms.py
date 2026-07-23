from django import forms
from .models import Category

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
