from django.shortcuts import render, redirect, get_object_or_404
from .models import Propietario, Mascota, Vacuna, HistorialVacuna, Especie
from .forms import PropietarioForm, MascotaForm, BusquedaForm, VacunaForm, EspecieForm  # Corrigido aquí

# Vista de inicio
def inicio(request):
    return render(request, 'vacunacion/inicio.html')

# Vista para registrar propietario
def registrar_propietario(request):
    if request.method == 'POST':
        form = PropietarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio después de guardar
    else:
        form = PropietarioForm()
    return render(request, 'vacunacion/registrar_propietario.html', {'form': form})

# Vista para registrar mascota
def registrar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio después de guardar
    else:
        form = MascotaForm()
    return render(request, 'vacunacion/registrar_mascota.html', {'form': form})

# Vista para registrar especie
def registrar_especie(request):
    if request.method == 'POST':
        form = EspecieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio después de guardar
    else:
        form = EspecieForm()
    return render(request, 'vacunacion/registrar_especie.html', {'form': form})

# Vista para registrar vacuna
def registrar_vacuna(request):
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio después de guardar
    else:
        form = VacunaForm()
    return render(request, 'vacunacion/registrar_vacuna.html', {'form': form})

# Vista para buscar una mascota por ID o cédula de propietario
def buscar_mascota(request):
    mascota = None
    propietario = None
    if request.method == 'GET':
        form = BusquedaForm(request.GET)
        if form.is_valid():
            id_mascota = form.cleaned_data.get('id_mascota')
            cedula_propietario = form.cleaned_data.get('cedula')

            # Búsqueda por ID de mascota
            if id_mascota:
                mascota = get_object_or_404(Mascota, id=id_mascota)
                propietario = mascota.propietario

            # Búsqueda por cédula de propietario
            elif cedula_propietario:
                propietario = get_object_or_404(Propietario, cedula=cedula_propietario)
                mascota = Mascota.objects.filter(propietario=propietario).first()

    else:
        form = BusquedaForm()
    
    return render(request, 'vacunacion/buscar_mascota.html', {
        'form': form,
        'mascota': mascota,
        'propietario': propietario
    })

# Vista para consultar el carnet de vacunación de una mascota
def consultar_carnet(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    historial_vacunas = HistorialVacuna.objects.filter(historial_medico__mascota=mascota)

    return render(request, 'vacunacion/carnet_vacunacion.html', {
        'mascota': mascota,
        'historial_vacunas': historial_vacunas
    })
