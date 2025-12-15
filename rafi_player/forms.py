from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nama', 'negara', 'usia', 'tinggi', 'berat', 'posisi','thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tambahkan styling Tailwind ke semua field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': (
                    'w-full p-3 rounded-lg bg-gray-800 text-white '
                    'border border-gray-700 focus:ring-2 focus:ring-green-500 focus:outline-none'
                )
            })