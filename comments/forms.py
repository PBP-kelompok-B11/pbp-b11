from django.forms import ModelForm
from .models import Comments

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['isi_komentar']
        widgets = {
            'isi_komentar': ModelForm.TextArea(attrs={
                'class': 'w-full p-3 rounded-lg text-indigo-900 border border-gray-300 focus:ring-2 focus:ring-lime-400 focus:outline-none',
                'placeholder': 'Tulis komentar kamu di sini...',
                'rows': 4
            }),
        }
        labels = {
            'isi_komentar': '',
        }