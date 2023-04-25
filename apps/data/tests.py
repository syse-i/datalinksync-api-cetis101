import pprint
import time
import os
import json
import threading

from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status

from .models import Data
from .serializers import DataSerializer

from apps.sync.helpers import worker_handler
from apps.sync.models import SyncContent

current_value = None


def worker_callback(connection, auto_close: bool = False):
    global current_value
    #print("worker_callback", current_value)
    def callback(channel, method, properties, body):
        global current_value

        try:
            # Atrapa el error de que el usuario no a sido creado
            data = json.loads(body)
            # print(data)
            # print(User.objects.all())
            # user = User.objects.get(pk=data["user_id"])
            # TODO: hacer que esto sea dinamico, que se pueda cambiar el modelo en base a content_type
            # instance = Data.objects.get(pk=data["object_id"])
            # sync_obj, created = instance.sync.get_or_create(user=user)
            # sync_obj.is_synced = False
            # sync_obj.save()
            channel.basic_ack(delivery_tag=method.delivery_tag)
            if auto_close:
                channel.close()
                connection.close()
                #print("worker_callback.callback",data)
                current_value = data
            return True
        except Exception as ex:
            print(ex)

        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return callback


# Mandanos a llamar a modelo User
User = get_user_model()


def assign_user_permission(user: User, model: models.Model, permission_codename: str):
    """
    añade permisos para de autorizacion 
    """
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(
        codename=permission_codename,
        content_type=content_type
    )
    user.user_permissions.add(permission)


def default_data(name: str = 'alexis'):
    """
    Se genera informacion para data para probar las validaciones del serializer
    """
    return {'name': name}


def test_func(name: str = ''):
    """
    Espero el valor que devulve wrapper
    """
    def wrapper():
        """
        verifica que alla un error en el valor proporcionado
        """
        data = default_data(name=name)
        serializer = DataSerializer(data=data)
        return serializer.is_valid(raise_exception=True)
    return wrapper


class DataSerializerTestCast(TestCase):
    # Pruebas unitarias de User

    def setUp(self):
        User.objects.create_user(
            username="foobar", email="foobar@noreplay.com", password="Eracj.123")

    def test_data_simple(self):  # Aqui se hace la prueba basica
        serializer = DataSerializer(data=default_data())
        response = serializer.is_valid(raise_exception=False)
        serializer.save()
        self.assertTrue(response)

    def test_name_is_required(self):
        """
        Prueba que no este vacio,(Prueba por defecto de django)
        """
        self.assertRaises(ValidationError, test_func(name=''))

    # Aui se hacen las pruebas de Del serialaizer UserSerializer
    def test_name_minimum(self):
        """
        verifica la validacion validate_word_minimum
        """
        self.assertRaises(ValidationError, test_func(name='al'))

    def test_special_characters(self):
        """
        verifica la validacion validate_special_characters
        """
        self.assertRaises(ValidationError, test_func(name='alexis-'))


class DataModelTest(TestCase):

    def setUp(self):
        """
        Se crea un usuario antes de epezar las pruebas 
        """
        user = User.objects.create_user(
            username="foobar",
            email="foobar@noreplay.com",
            password="Eracj.123",
        )
        assign_user_permission(user, Data, 'add_data')

    # def tearDown(self):
    #     exit()

    # Pruebas de sincronizacion

    def test_create_data_sync(self):
        """
        esta prueba verifica que el post de data funcione
        """

        client = APIClient()
        client.login(username='foobar', password='Eracj.123')

        response = client.post('/v1/CetisAlumnos/',
                               default_data(), format='json')

        self.assertTrue(Data.objects.filter(name='alexis').exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_sync(self):
        global current_value
        """
        esta prueba verifica que el post de User funcione correctamente
        seguido de que la data se sincronize
        """
        with self.settings(RABBIT_CHANNEL='mock_update_sync_content'):
            def blocker():
                from django.conf import settings
                worker_handler(settings.RABBIT_CHANNEL,
                               worker_callback, auto_close=True)

            t = threading.Thread(name='child procs', target=blocker)
            t.start()

            client = APIClient()
            client.login(username='foobar', password='Eracj.123')
            User.objects.create_user(
                username="alexis",
                email="alexis@noreplay.com",
                password="Eracj.123"
            )
            response = client.post('/v1/CetisAlumnos/',
                                   default_data(), format='json')
            #print(Data.objects.first().id)
            #print("response", response.json())
            #print("callback", current_value)

            # print('first ',SyncContent.objects.first())
            self.assertTrue(User.objects.filter(username='foobar').exists())
            # self.assertTrue(SyncContent.objects.first())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_permission(self):
        """
        verifica que el permizo data_add sea requerido
        """
        client = APIClient()
        client.login(username='alexis', password='Eracj.123')

        response = client.post('/v1/CetisAlumnos/',
                               default_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_2 = client.get('/v1/CetisAlumnos/')
        self.assertEqual(response_2.status_code, status.HTTP_401_UNAUTHORIZED)
