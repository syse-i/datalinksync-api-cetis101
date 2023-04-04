from django.contrib import admin

from apps.data.models import Data

# Register your models here.

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

