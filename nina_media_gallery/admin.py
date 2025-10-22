from django.contrib import admin
from .models import Media

# Register your models here.
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['category', 'deskripsi']
    search_fields = ['category']
    list_filter = ['category', 'created_at']