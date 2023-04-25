import pika
import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from apps.data.models import Data

from . import WorkerCommand

from ...helpers import worker_callback

User = get_user_model()#mandamos a llamar el modelo User


class Command(WorkerCommand):#Mandamos a llamar la clase WorkerCommand estable la conexion con RabbitMQ
    """
    recibe los puertos y manda las colas a rabbitmq
    """
    help = ''
    queue_name = settings.RABBIT_CHANNEL

    def callback(self, *args, **kwargs):
        return worker_callback(*args, **kwargs)
