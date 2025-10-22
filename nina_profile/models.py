from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator

# Create your models here.
User = get_user_model()

class ProfileWidget(models.Model):
    JENIS_WIDGET = [
        ('chart', 'Chart'),
        ('statistik', 'Statistik'),
    ]
    # Relasi generik agar model ini bisa terhubung dengan model Player atau Club
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('player', 'club')})     # mencari jenis model yang digunakan (player atau club)
    object_id = models.PositiveIntegerField()   # id dari model target
    profil = GenericForeignKey('content_type', 'object_id')
    widget_types = models.CharField(max_length=20, choices=JENIS_WIDGET, default='chart')
    konfigurasi = models.JSONField(blank=True, default=dict, help_text='JSON config for the widget (e.g. {"seasons": ["2022/23"], "metric": "goals"})')
    title = models.CharField(max_length=120, blank=True)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        target = f"{self.content_type}#{self.object_id}"
        return f"Widget {self.pk} for {target} ({self.widget_types})"
    