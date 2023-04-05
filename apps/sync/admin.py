from django.contrib import admin

from .models import SyncContent

# Register your models here.

@admin.register(SyncContent)
class SyncContentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'content_type',
        'object_id',
        'is_synced',
        'created',
        'modified'
    ]
    search_fields = ["user__email", "user__username"]