from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isi_komentar = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    # GenericForeignKey untuk relasi ke model manapun (Player dan Club)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=36)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username}: {self.isi_komentar[:30]}"
