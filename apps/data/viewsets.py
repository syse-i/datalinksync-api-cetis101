from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import Data
from .serializers import DataSerializer

class DataViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):#Configuracion de filtros 
    serializer_class = DataSerializer
    #Fitros de v1/CetisAlumnos/
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fidels = ["name"]

    def get_queryset(self):#Nos permite mostrar informacion en el url v1/
        return Data.objects.filter(
            sync__user=self.request.user, 
            sync__is_synced=False
        ).distinct()
    
