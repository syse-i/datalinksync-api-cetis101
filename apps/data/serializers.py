import re

from rest_framework import serializers
from apps.data.models import Data
from rest_framework.exceptions import ValidationError

def validate_word_minimum(value):
    if len(value) <= 2:
        raise ValidationError("El nombre es mu corto")
    return value


def validate_special_characters(value, message=None):
    if message is None:
        message = 'El campo no debería de tener caracteres especiales'
    if not bool(re.match("[a-zA-Z\s]+$", value)):
        raise ValidationError(message)
    return value


class UserDataSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        return validate_word_minimum(validate_special_characters(value))

    class Meta:
        model = Data
        fields = [
            'id',
            'name',
        ]