from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'alamat', 'umur', 'nomor_handphone')
    search_fields = ('user__username', 'alamat', 'nomor_handphone')
    readonly_fields = ('user', 'alamat', 'umur', 'nomor_handphone')
    
    def has_add_permission(self, request):
        # Mencegah tambah data dari admin
        return False

    def has_change_permission(self, request, obj=None):
        # Mencegah edit data dari admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Mencegah hapus data dari admin
        return False
from .models import Media

# Register your models here.
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['category', 'deskripsi']
    search_fields = ['category']
    list_filter = ['category', 'created_at']
