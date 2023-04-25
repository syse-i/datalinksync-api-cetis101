import pika
import json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...helpers import worker_handler

# def callback(ch, method, properties, body):
#     try:
#         data = json.loads(body)
#         print(data)
#         instance = Data.objects.get(pk=data["object_id"])
#         sync_obj, created = instance.sync.get_or_create(user_id=data["user_id"])
#         sync_obj.is_synced = False
#         sync_obj.save()
#     except Data.DoesNotExist as ex:
#         print(ex)


class WorkerCommand(BaseCommand):
    """
    genera las colas en rabbitmq 
    """
    help = ''
    queue_name: str = ''

    def callback(ch, method, properties, body):
        raise CommandError("No me definiste, muy mal...")

    def handle(self, *args, **options):#Establece la conexion con RabbitMQ
        """
        genera las colas cuando termina se cierra las colas  
        """
        worker_handler(self.queue_name, self.callback)
        self.stdout.write(self.style.SUCCESS('RabbitMQ worker connection closed'))
