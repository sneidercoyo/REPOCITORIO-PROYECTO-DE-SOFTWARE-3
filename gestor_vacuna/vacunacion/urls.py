from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import (
    inicio,
    registrar_propietario,
    registrar_mascota,
    registrar_especie,
    registrar_vacuna,
    buscar_mascota,
    consultar_carnet,
    servicios,
    nosotros,
    login_veterinarios,
    login_usuarios,
)

urlpatterns = [
    # URLs principales
    path('', inicio, name='inicio'),  # Vista para la página de inicio
    path('registrar-propietario/', registrar_propietario, name='registrar_propietario'),
    path('registrar-mascota/', registrar_mascota, name='registrar_mascota'),
    path('registrar-especie/', registrar_especie, name='registrar_especie'),
    path('registrar-vacuna/', registrar_vacuna, name='registrar_vacuna'),
    path('buscar-mascota/', buscar_mascota, name='buscar_mascota'),
    path('consultar-carnet/<int:mascota_id>/', consultar_carnet, name='consultar_carnet'),

    # Nuevas URLs que has agregado
    path('servicios/', servicios, name='servicios'),
    path('nosotros/', nosotros, name='nosotros'),
    
    # URLs de login y logout
    path('login_medicos/', views.login_medicos, name='login_medicos'),
    path('login_veterinarios/', login_veterinarios, name='login_veterinarios'),
    path('login_usuarios/', login_usuarios, name='login_usuarios'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
]
