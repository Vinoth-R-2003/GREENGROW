from django import forms
from .models import PlantCheck


class PlantCheckForm(forms.ModelForm):
    class Meta:
        model = PlantCheck
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'class': 'hidden',
                'id': 'image-input',
            }),
        }

class CropRecommendationForm(forms.ModelForm):
    class Meta:
        model = PlantCheck
        fields = ['temperature', 'soil_type', 'rainfall', 'proposed_crop']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none', 'placeholder': 'e.g., 25.5', 'step': '0.1'}),
            'soil_type': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none', 'placeholder': 'e.g., Loamy, Clay, Sandy'}),
            'rainfall': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none', 'placeholder': 'e.g., 1200', 'step': '0.1'}),
            'proposed_crop': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none', 'placeholder': 'e.g., Wheat, Rice (Optional)'}),
        }
