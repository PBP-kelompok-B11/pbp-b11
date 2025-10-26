# events/forms.py
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'nama_event',
            'lokasi',
            'tanggal',
            'tim_home',
            'tim_away',
            'skor_home',
            'skor_away',
        ]
        widgets = {
            'nama_event': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Pertandingan atau Event'
            }),
            'lokasi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lokasi Pertandingan'
            }),
            'tanggal': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'tim_home': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tim Tuan Rumah'
            }),
            'tim_away': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tim Tamu'
            }),
            'skor_home': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'skor_away': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }
        labels = {
            'nama_event': 'Nama Event',
            'lokasi': 'Lokasi',
            'tanggal': 'Tanggal',
            'tim_home': 'Tim Home',
            'tim_away': 'Tim Away',
            'skor_home': 'Skor Tim Home',
            'skor_away': 'Skor Tim Away',
        }

    def clean(self):
        cleaned_data = super().clean()
        skor_home = cleaned_data.get('skor_home')
        skor_away = cleaned_data.get('skor_away')

        if skor_home is not None and skor_home < 0:
            self.add_error('skor_home', 'Skor tidak boleh negatif.')
        if skor_away is not None and skor_away < 0:
            self.add_error('skor_away', 'Skor tidak boleh negatif.')

        return cleaned_data
