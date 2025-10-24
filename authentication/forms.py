from django.forms import Media, ModelForm

class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ["deksripsi", "category", "thumbnail"]