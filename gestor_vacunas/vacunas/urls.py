from django.urls import path
from .views import *

urlpatterns = [
    path('', listar_mascotas, name='listar_mascotas'),
    path('mascotas/nuevo/', crear_mascota, name='crear_mascota'),
    path('vacunas/', listar_vacunas, name='listar_vacunas'),
    path('vacunas/nuevo/', crear_vacuna, name='crear_vacuna'),
    path('citas/', listar_citas, name='listar_citas'),
    path('citas/nuevo/', crear_cita, name='crear_cita'),
    path('historial-medico/', listar_historial_medico, name='listar_historial_medico'),
    path('historial-medico/nuevo/', crear_historial_medico, name='crear_historial_medico'),
]
