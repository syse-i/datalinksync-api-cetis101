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

User = get_user_model()#Llamamos la Usuarios

class Data(TimeStampedModel):#Tabla Data
    id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=256)

    sync = GenericRelation(SyncContent)#Relacion Generica para sincronizar informacion

    def __str__(self):
        return self.name


# method for updating
@receiver(post_save, sender=Data, dispatch_uid="sync_by_data_content")#Esto se ejecuta cuando Data crea o actuliza informacion.
def update_data(sender, instance: Data, **kwargs):#Esta funcion define callback y llama la funcion update_data_signal manda los parametros nombre de cola, funcion callback. 
    def callback(basic_publish):#Esta funcion guarda la nueva data para los usuarion.
        for user in User.objects.all():
            basic_publish({
                'content_type': 'data',
                'object_id': str(instance.id),
                'user_id': str(user.id)
            })

    update_data_signal('update_sync_content', callback)#Ejecuta la funcion update_data_signal.


@receiver(post_save, sender=User, dispatch_uid="sync_by_user_content")#Esto se ejecuta cuando se crea un nuevo usuario.
def update_user(sender, instance: User, created, **kwargs):
    if created:#valida que se este creado un usuario.
        def callback(basic_publish):#Actualiza la Informacion del usuario que hay actualmente.
            for data in Data.objects.all():
                basic_publish({
                    'content_type': 'data',
                    'object_id': str(data.id),
                    'user_id': str(instance.id)
                })
        
        update_data_signal('update_sync_content', callback)#Ejecuta la funcion update_data_signal.

