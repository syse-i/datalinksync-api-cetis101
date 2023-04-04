from django.test import TestCase

from apps.data.serializers import UserDataSerializer
from rest_framework.exceptions import ValidationError

def default_data(name:str = 'alexis'):
    return {'name': name}


def test_func(name:str = ''):
    def wrapper():
        data = default_data(name=name)
        serializer = UserDataSerializer(data=data)
        return serializer.is_valid(raise_exception=True)
    return wrapper


class UserDataTestCast(TestCase):

    def test_simple_data(self):
        serializer = UserDataSerializer(data=default_data())
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_name_minimum(self):
        self.assertRaises(ValidationError, test_func(name='al'))

    def test_name_is_required(self):
        self.assertRaises(ValidationError, test_func(name=''))