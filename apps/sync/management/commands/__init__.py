import pika
import json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

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
        try:#Atrapa Errores
            connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300))
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
            self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
            channel.close()
        except KeyboardInterrupt:#Si se interupe el proseso salta el error
            pass
        #finally:#Si se finaliza el proseso cierra la conexion con RabbitMQ
