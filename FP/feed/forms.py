from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Share your harvest update...',
                'class': 'flex-1 bg-slate-50 border-none rounded-full px-6 py-3 focus:ring-2 focus:ring-emerald-500 transition-all outline-none w-full'
            }),
            'image': forms.FileInput(attrs={'class': 'hidden', 'id': 'post-image-input'})
        }
