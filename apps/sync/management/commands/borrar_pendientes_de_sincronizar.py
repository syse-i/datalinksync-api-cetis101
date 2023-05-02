from django.core.management.base import BaseCommand, CommandError

from apps.sync.models import SyncContent  


class Command(BaseCommand):
    help = """
    Cambiamos el estado de sincronización de todos los registros activos, 
    para que se puedan consultar nuevamente
    """

    def handle(self, *args, **options):
        SyncContent.objects.all().update(is_synced=False)
        return print('Successfully')