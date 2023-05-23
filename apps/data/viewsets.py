# Python libs

# Django libs


# Third party libs
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from rest_framework import status
from rest_framework.decorators import action

# Local libs
from .models import Data
from .serializers import DataSerializer

# Internal local libs
from apps.sync.models import SyncContent


class DataViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API Class
    ---------
    La API tiene paginacion de 20, tiene
    filtros como field filters,search fields,
    ordering fidels y puedes crear en data 
    en el campo data ,"REQUIERE EL TOKEN PARA FUNCIONAR"

    Parametros
    ----------
    name : str 

    el nombre debe tener como minimo 3 caracteres 
    ademas de que no puede contener caracteres 
    especiales como (/%&$_#-)
    """

    # Configuracion de filtros
    serializer_class = DataSerializer
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fidels = ["name"]
    # Nos permite mostrar informacion en el url v1/ con la ayuda de los mixins

    def get_queryset(self):
        """
        devuelve filtro de data
        """
        return Data.objects.filter(
            sync__user=self.request.user,
            sync__is_synced=False
        ).order_by('-modified').distinct()

    def list(self, request, *args, **kwargs):
        """
        Filtros
        -------
        -searsh fields

        -filterset fields

        -ordering fidels

        Permisos de usuario
        -------------------
        -Se requiere el permizo de usuario de view en data para poder consultar
        """
        if not self.request.user.has_perm("data.view_data"):
            raise NotAcceptable("El usuario no tiene permisos")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Permisos de usuario
        -------------------
        Se requiere el permizo de usuario de add para poder añadir nueva informacion
        """
        if not self.request.user.has_perm("data.add_data"):
            raise NotAcceptable("El usuario no tiene permisos")
        return super().create(request, *args, **kwargs)

    @action(methods=["PATCH"], detail=False)
    def mark_as_read(self, request, *args, **kwargs):
        """
        Actualiza que la informacion ya a sido sincronizada 
        y no actualize todo de nuevo  
        """
        queryset = self.filter_queryset(self.get_queryset())        
        page = self.paginate_queryset(queryset)

        print(page)

        # SyncContent.objects.filter(id__in=[data.id for data in queryset]).update(is_synced=True)
        SyncContent.objects.filter(
            object_id__in=[data.id for data in page]).update(is_synced=True)

        # if page is not None:
        #     SyncContent.objects.filter(id__in=[data["id"] for data in page]).update(is_synced=True)
        # else:

        return Response(status=status.HTTP_202_ACCEPTED)
