from django.contrib import admin
from .models import UserProfile
from nina_media_gallery.models import Media


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'alamat', 'umur', 'nomor_handphone', 'role')
    search_fields = ('user__username', 'alamat', 'nomor_handphone')
    readonly_fields = ('user', 'alamat', 'umur', 'nomor_handphone')

    def _is_admin(self, request):
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin':
            return True
        
        return False
    
    def has_add_permission(self, request):
        # Mencegah tambah data dari admin
        return self._is_admin(request)

    def has_change_permission(self, request, obj=None):
        # Mencegah edit data dari admin
        return self._is_admin(request)

    def has_delete_permission(self, request, obj=None):
        # Mencegah hapus data dari admin
        return self._is_admin(request)
    
    def get_readonly_fields(self, request, obj = None):
        if not self._is_admin(request):
            return ('user', 'alamat', 'umur', 'nomor_handphone', 'role')
        return()


