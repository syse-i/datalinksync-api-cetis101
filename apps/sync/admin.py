from django.contrib import admin

from .models import SyncContent

# Register your models here.


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