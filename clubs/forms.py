from django import forms
from .models import Club, Ranking

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['nama', 'negara', 'stadion', 'tahun_berdiri']

class RankingForm(forms.ModelForm):
    class Meta:
        model = Ranking
        fields = ['musim', 'peringkat']
