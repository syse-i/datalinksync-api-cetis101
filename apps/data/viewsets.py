from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import Data
from .serializers import UserDataSerializer

class DataViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        return Data.objects.all()

