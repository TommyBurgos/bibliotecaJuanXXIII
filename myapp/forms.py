from django.forms import ModelForm
from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['nombre', 'fechaPublicacion', 'descripcion', 'generos', 'imgPortada', 'autor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaPublicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'generos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'imgPortada': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'})
        }