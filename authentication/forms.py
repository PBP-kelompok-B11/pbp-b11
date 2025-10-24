from django.forms import ModelForm

class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ["deksripsi", "category", "thumbnail"]