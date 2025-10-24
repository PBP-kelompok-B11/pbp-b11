from django.contrib import admin
from .models import SearchQuery


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('kata_kunci', 'jenis', 'user', 'tanggal')
    list_filter = ('jenis', 'tanggal')
    search_fields = ('kata_kunci', 'user__username')
    ordering = ('-tanggal',)
    readonly_fields = ('kata_kunci', 'jenis', 'user', 'tanggal')

    def has_add_permission(self, request):
        """Agar admin tidak bisa nambah manual search record (harus dari user)."""
        return False

    def has_change_permission(self, request, obj=None):
        """Agar admin hanya bisa lihat, tidak bisa ubah record pencarian."""
        return False

