from django.contrib import admin
from .models import Club, ClubRanking

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nama', 'negara', 'stadion', 'tahun_berdiri')
    search_fields = ('nama', 'negara', 'stadion')

@admin.register(ClubRanking)
class ClubRankingAdmin(admin.ModelAdmin):
    list_display = ('club', 'musim', 'peringkat')
    list_filter = ('musim',)
    search_fields = ('club__nama',)
