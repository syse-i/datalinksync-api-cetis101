import uuid
import json
import time
from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from apps.sync.models import SyncContent
from apps.sync.signals import update_data_signal
import pika

User = get_user_model()  # Llamamos la Usuarios

"""
Aqui creamos las tablas en la base de datos
mediante clases
"""


class Data(TimeStampedModel):  # Tabla Data
    """
    Parametros
    ----------
    name : str

    Se espera un nombre

    sync : class

    Espera el modelo(SyncContent), Para sincronizar la informacion
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=256)
    sync = GenericRelation(SyncContent)

    def __str__(self):
        return self.name


"""
@receiver : se ejecuta cuando se genera un post es decir 
cuando se crea nueva o actualiza informacion en la base de datos.
"""

# method for updating

"""
Es receiver se ejecuta cuando se actualiza la informacion en Data
"""


@receiver(post_save, sender=Data, dispatch_uid="sync_by_data_content")
def update_data(sender, instance: Data, **kwargs):
    """
    Esta funcion define callback y llama la funcion update_data_signal
    manda los parametros nombre de la cola y callback 
    ('update_sync_content', callback), para comenzar la sicronizacion 
    de datos para los usuarios.
    """
    def callback(basic_publish):
        """
        Esta funcion guarda la nueva informacion de data para los usuarios
        """
        for user in User.objects.all():
            basic_publish({
                'content_type': 'data',
                'object_id': str(instance.id),
                'user_id': str(user.id)
            })
    update_data_signal('update_sync_content', callback)


"""
Es receiver se ejecuta cuando se actualiza la informacion en User
"""


@receiver(post_save, sender=User, dispatch_uid="sync_by_user_content")
def update_user(sender, instance: User, created, **kwargs):
    """
    Esta funcion solo se utiliza cuando se crea un nuevo usuario
    llama la funcion update_data_signal y toma los parametros de
    callback manda el nombre de la cola
    ('update_sync_content', callback), y sincroniza los datos
    para los usuario nuevo
    """
    if created:
        def callback(basic_publish):
            """
            Esta funcion guarda la nueva informacion de data para el nuevo
            usuario
            """
            for data in Data.objects.all():
                basic_publish({
                    'content_type': 'data',
                    'object_id': str(data.id),
                    'user_id': str(instance.id)
                })
        # Ejecuta la funcion update_data_signal.
        update_data_signal('update_sync_content', callback)
