import re

from rest_framework import serializers
from apps.data.models import Data
from rest_framework.exceptions import ValidationError

def validate_word_minimum(value):#Valida que el nombre tenga mas de dos letras
    """
    La validacion pide como minimo 3 caracteres en name
    """
    if len(value) <= 2:
        raise ValidationError("El nombre es mu corto")
    return value


def validate_special_characters(value, message=None):#Valida que no tenga caracteres especiales
    """
    Esta validacion solo almite a-z en name, sino tirara error
    como respuesta
    """
    if message is None:
        message = 'El campo no debería de tener caracteres especiales'
    if not bool(re.match("[a-zA-Z\s]+$", value)):#Esto se valida por Expreciones regulares
        raise ValidationError(message)
    return value


class DataSerializer(serializers.ModelSerializer):
    """
    Aui validamos los campos de data mandando a llamar las funciones
    """

    def validate_name(self, value):
        """
        manda el parametro name a la funciones
        validate_word_minimum y validate_special_characters
        """
        return validate_word_minimum(validate_special_characters(value))#Se manda a llamar las validaciones y se manda el parametro

    class Meta:
        """
        Declaramos los parametros que usaremos del modelo
        """
        model = Data
        fields = [
            'id',
            'name',
        ]