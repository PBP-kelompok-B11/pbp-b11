from django import forms
from .models import Club, ClubRanking

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['nama', 'negara', 'stadion', 'tahun_berdiri']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'negara': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'stadion': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'tahun_berdiri': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
        }


class ClubRankingForm(forms.ModelForm):
    class Meta:
        model = ClubRanking
        fields = ['musim', 'peringkat']
        widgets = {
            'musim': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'peringkat': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
        }
