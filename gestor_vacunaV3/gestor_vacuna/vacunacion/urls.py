from django.urls import path
from .views import (
    inicio,
    registrar_propietario,
    registrar_mascota,
    registrar_especie,
    registrar_vacuna,
    buscar_mascota,
    consultar_carnet,
)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registrar-propietario/', registrar_propietario, name='registrar_propietario'),
    path('registrar-mascota/', registrar_mascota, name='registrar_mascota'),
    path('registrar-especie/', registrar_especie, name='registrar_especie'),
    path('registrar-vacuna/', registrar_vacuna, name='registrar_vacuna'),
    path('buscar-mascota/', buscar_mascota, name='buscar_mascota'),
    path('consultar-carnet/<int:mascota_id>/', consultar_carnet, name='consultar_carnet'),
]
