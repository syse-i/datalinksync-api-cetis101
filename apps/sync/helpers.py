import time
import pika
import json

from django.conf import settings

from apps.data.models import Data, User

def worker_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300))


def worker_handler(queue_name: str, callback: callable, auto_close: bool = False):
    try:
        # Atrapa Errores
        connection = worker_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(queue=queue_name, on_message_callback=callback(connection, auto_close))
        print(f'[{queue_name}] [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        # Si se interupe el proseso salta el error
        pass


def worker_callback(connection, auto_close: bool = False):
    def callback(channel, method, properties, body):
        attempts = 5
        pivot = 0

        while pivot < attempts:
            try:
                # Atrapa el error de que el usuario no a sido creado
                data = json.loads(body)
                user = User.objects.get(pk=data["user_id"])
                # TODO: hacer que esto sea dinamico, que se pueda cambiar el modelo en base a content_type
                instance = Data.objects.get(pk=data["object_id"])
                sync_obj, created = instance.sync.get_or_create(user=user)
                sync_obj.is_synced = False
                sync_obj.save()
                channel.basic_ack(delivery_tag=method.delivery_tag)
                if auto_close:
                    channel.close()
                    return connection.close()
                return True
            except Data.DoesNotExist as ex:
                if settings.DEBUG:
                    print(f"Intentando({pivot}) nuevamente debido a que el dato todavia no existe")
            except User.DoesNotExist:
                if settings.DEBUG:
                    print(f"Intentando({pivot}) nuevamente debido a que el usuario todavia no existe")
            finally:
                time.sleep(1)
                pivot += 1
        
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback