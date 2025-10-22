from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nama', 'negara', 'usia', 'tinggi', 'berat', 'posisi']
