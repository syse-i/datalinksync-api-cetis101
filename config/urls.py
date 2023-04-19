"""Cetis_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, urls
from apps.data.viewsets import DataViewSet
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

#Configuracion del url
router = routers.DefaultRouter()
router.register('CetisAlumnos', DataViewSet,'CetisAlumno')

#Aqui añadimos los urls
urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),#Panel de Administracion de django por defecto
    path('api-auth/', include('rest_framework.urls')),#Interfaz rest_framework
    path('v1/', include(router.urls)),#Get y Post y Filtros de data
    path('openapi', get_schema_view(
        title="Cetis 101",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger/index.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc/index.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'), 
]

