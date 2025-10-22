from django import forms
from .models import ProfileWidget
from django.contrib.contenttypes.models import ContentType

class ProfileWidgetForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.filter(model__in=['player', 'club']), required=True, help_text='Choose model (Player or Club)')

    class Meta:
        model = ProfileWidget
        fields = ['title', 'widget_types', 'konfigurasi', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'konfigurasi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }