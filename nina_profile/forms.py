from django import forms
from .models import ProfileWidget
from django.contrib.contenttypes.models import ContentType

class ProfileWidgetForm(forms.ModelForm):
    # Untuk memilih model target (Club atau Player)
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=['player', 'club']),
        required=True,
        label="Pilih Tipe Model (Player / Club)"
    )

    class Meta:
        model = ProfileWidget
        fields = ['title', 'widget_type', 'konfigurasi', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul widget'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deskripsi tambahan (opsional)'}),
            'konfigurasi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '{"season": "2022/23", "metric": "goals"}'}),
            'widget_type': forms.Select(attrs={'class': 'form-select'}),
        }
