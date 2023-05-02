from django.contrib import admin

from .models import SyncContent


@admin.action(description="Marcar como sincronizado(false)")
def make_sync_false(modeladmin, request, queryset):
    queryset.update(is_synced=False)


@admin.action(description="Marcar como sincronizado(true)")
def make_sync_true(modeladmin, request, queryset):
    queryset.update(is_synced=True)

@admin.register(SyncContent)
class SyncContentAdmin(admin.ModelAdmin):
    """
    Añadimos el modelo SyncContet a panel de adminnistracion
     y integramos el Fitro search
    """
    list_display = [
        'user',
        'content_type',
        'object_id',
        'is_synced',
        'created',
        'modified'
    ]
    search_fields = ["user__email", "user__username"]
    actions = [make_sync_false, make_sync_true]