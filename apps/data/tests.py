from pprint import pprint
from django.test import TestCase

from apps.data.serializers import DataSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


# Mandanos a llamar a modelo User
User = get_user_model()


def default_data(name:str = 'alexis'):
    """
    Se genera informacion para data para probar las validaciones del serializer
    """
    return {'name': name}


def test_func(name:str = ''):
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

class DataSerializerTestCast(TestCase):#Pruebas unitarias de User

    def setUp(self):
        User.objects.create_user(username="foobar", email="foobar@noreplay.com", password="Eracj.123")

    def test_data_simple(self):#Aqui se hace la prueba basica
        serializer = DataSerializer(data=default_data())
        response = serializer.is_valid(raise_exception=False)
        pprint(response)
        serializer.save()
        self.assertTrue(response)

    def test_name_is_required(self):
        """
        Prueba que no este vacio,(Prueba por defecto de django)
        """
        self.assertRaises(ValidationError, test_func(name=''))
   
    #Aui se hacen las pruebas de Del serialaizer UserSerializer
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