import uuid
from django.db import models

# Create your models here.
class Media(models.Model):
    CATEGORY_CHOICES = [
        ('foto', 'Photo'),
        ('video', 'Video'),
    ]

    deskripsi = models.TextField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='foto')
    thumbnail = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    viewers = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def increment_views(self):
        self.viewers += 1
        self.save()
