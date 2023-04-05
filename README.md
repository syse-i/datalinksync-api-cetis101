# Introduccion

    Estoy creando un proyecto de django para crear una api
    para guardar informacion local 

------

# Como crear una aplicacion de djanto

## Instala Django

    pip3 install Django==4.2

## Crear base del proyecto

    django-admin startproject AquiVaElNombreDelProyecto

# Instalacion (django-rest-framework)

   pip3 install djangorestframework

------

# Como crear una app

    python3 manage.py startapp AquiVaElNombreDeLaApp

# Como hacer una API

## Paso 1, Generar la primera migracion

    python3 manage.py migrate

## Paso 2, Crear Un superUsuario

    python3 manage.py createsuperuser

## Paso 3, Correr el proyecto

    python3 manage.py runserver 

## Acceder al panel de administración
```
python3 manage.py createsuperuser
```

    Acceder al url: http://localhost:8000/admin

    
- MODELS

    Creamos la primera tabla llamada Data mediante una clase



- VIEWSETS

### Paso 1, Creamos el archivo viewsets.py en la carpeta data

    Importamos UserDaraSerialazer

### Paso 2, Cramos una funcion

    En esta funcion se ara una consulta a la base de datos
    
    
- URLS

### Paso 1

    Importamo Routers de rest_framework y UserDataViewSets

### Paso 2

    Despues realizamos el Url con UserDataViewSets


---

- SERIALIZERS

### Paso 1

    Creamos El serializer y la Clase meta 

---
## Instalación

```
pip3 install -r requirements.txt