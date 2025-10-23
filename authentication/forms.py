from django.forms import ModelForm
from nina_media_gallery.models import Media

class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ["deskripsi", "category", "thumbnail"]