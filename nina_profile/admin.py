from django.contrib import admin
from .models import ProfileWidget

# Register your models here.
@admin.register(ProfileWidget)
class ProfileWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'widget_types', 'content_type', 'object_id', 'created_by', 'updated_at')
    list_filter = ('widget_types', 'content_type')
    search_fields = ('title',)
    
