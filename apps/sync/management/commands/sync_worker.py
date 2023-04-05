import pika
import json
import time
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from apps.data.models import Data

from . import WorkerCommand

User = get_user_model()#mandamos a llamar el modelo User


class Command(WorkerCommand):#Mandamos a llamar la clase WorkerCommand estable la conexion con RabbitMQ
    help = ''
    queue_name = 'update_sync_content'

    def callback(self, ch, method, properties, body):
        attempts = 5
        pivot = 0

        while pivot < attempts:
            try:#Atrapa el error de que el usuario no a sido creado
                data = json.loads(body)
                print(data)
                user = User.objects.get(pk=data["user_id"])
                # TODO: hacer que esto sea dinamico, que se pueda cambiar el modelo en base a content_type
                instance = Data.objects.get(pk=data["object_id"])
                sync_obj, created = instance.sync.get_or_create(user=user)
                sync_obj.is_synced = False
                sync_obj.save()
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return True
            except Data.DoesNotExist as ex:
                print(ex)
                raise CommandError(ex)
            except User.DoesNotExist:
                time.sleep(1)
                print(f"Intentando({pivot}) nuevamente debido a que el usuario todavia no existe")
                pivot += 1
        
        raise Exception("Aqui sucedio algo")


