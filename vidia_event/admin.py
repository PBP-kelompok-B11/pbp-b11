from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_event', 'tipe', 'lokasi', 'tanggal_mulai', 'tanggal_selesai')
    list_filter = ('tipe', 'tanggal_mulai', 'tanggal_selesai')
    search_fields = ('nama_event', 'lokasi')
