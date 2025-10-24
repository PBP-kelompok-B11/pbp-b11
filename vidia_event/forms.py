# events/forms.py
from django import forms
from .models import Event, EventParticipation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nama_event', 'tipe', 'lokasi', 'tanggal_mulai', 'tanggal_selesai']
        widgets = {
            'nama_event': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Event'}),
            'tipe': forms.Select(attrs={'class': 'form-select'}),
            'lokasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lokasi'}),
            'tanggal_mulai': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_selesai': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nama_event': 'Nama Event',
            'tipe': 'Tipe Event',
            'lokasi': 'Lokasi',
            'tanggal_mulai': 'Tanggal Mulai',
            'tanggal_selesai': 'Tanggal Selesai',
        }


class EventParticipationForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ['player', 'club', 'peran', 'hasil']
        widgets = {
            'player': forms.Select(attrs={
                    'class': 'w-48 h-10 bg-lime-400 text-indigo-900 text-xl font-normal rounded-[36px] px-3'
                        }),
            'club': forms.Select(attrs={
                    'class': 'w-48 h-10 bg-lime-400 text-indigo-900 text-xl font-normal rounded-[36px] px-3'
                        }),
            'peran': forms.Select(attrs={
                    'class': 'w-48 h-10 bg-lime-400 text-indigo-900 text-xl font-normal rounded-[36px] px-3'
                        }),
            'hasil': forms.Select(attrs={
                    'class': 'w-48 h-10 bg-lime-400 text-indigo-900 text-xl font-normal rounded-[36px] px-3'
                        }),
        }
        labels = {
            'player': 'Pemain',
            'club': 'Klub',
            'peran': 'Peran',
            'hasil': 'Hasil',
        }

    def clean(self):
        """Validasi agar player dan club tidak kosong bersamaan."""
        cleaned_data = super().clean()
        player = cleaned_data.get('player')
        club = cleaned_data.get('club')

        if not player and not club:
            raise forms.ValidationError("Minimal isi salah satu: pemain atau klub.")

        return cleaned_data
    