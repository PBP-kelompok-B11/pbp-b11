from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'negara', 'posisi', 'usia', 'user')  # kolom yang ditampilkan
    list_filter = ('posisi', 'negara')  # filter di sidebar
    search_fields = ('nama', 'negara')  # search bar
    ordering = ('nama',)  # urutan default