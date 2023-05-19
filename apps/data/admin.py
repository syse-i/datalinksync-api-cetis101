from django.contrib import admin

from apps.data.models import Data

# Register your models here.



@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    """
    Aqui mostramos en el panel de administracion el modelo data
    """
    list_display = [
        'id',
        'name',
        'created',
        'modified',
    ]

    search_fields = ('name',)

