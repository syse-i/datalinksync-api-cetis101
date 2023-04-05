from django.contrib import admin

from apps.data.models import Data

# Register your models here.


#Aqui mostramos en el panel de administracion el modelo data
@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

