from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_event', 'lokasi', 'tanggal', 'tim_home', 'tim_away', 'skor_home', 'skor_away')
    list_filter = ('tanggal', 'lokasi')
    search_fields = ('nama_event', 'tim_home', 'tim_away', 'lokasi')
