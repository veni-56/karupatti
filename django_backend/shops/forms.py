from django import forms
from .models import Shop


class ShopCreateForm(forms.ModelForm):
    """Form for creating a new shop"""
    
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'banner', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your shop'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Shop email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shop address'}),
        }


class ShopUpdateForm(forms.ModelForm):
    """Form for updating shop details"""
    
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'banner', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
