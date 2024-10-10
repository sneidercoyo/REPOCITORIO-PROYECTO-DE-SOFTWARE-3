from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Vista para registrar mascotas
def listar_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'vacunas/listar_mascotas.html', {'mascotas': mascotas})

def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'vacunas/crear_mascota.html', {'form': form})

# Vista para listar y crear vacunas
def listar_vacunas(request):
    vacunas = Vacuna.objects.all()
    return render(request, 'vacunas/listar_vacunas.html', {'vacunas': vacunas})

def crear_vacuna(request):
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_vacunas')
    else:
        form = VacunaForm()
    return render(request, 'vacunas/crear_vacuna.html', {'form': form})

# Vista para listar y crear citas
def listar_citas(request):
    citas = Cita.objects.all()
    return render(request, 'vacunas/listar_citas.html', {'citas': citas})

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_citas')
    else:
        form = CitaForm()
    return render(request, 'vacunas/crear_cita.html', {'form': form})

# Historial médico
def listar_historial_medico(request):
    historiales = HistorialMedico.objects.all()
    return render(request, 'vacunas/listar_historial_medico.html', {'historiales': historiales})

def crear_historial_medico(request):
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_historial_medico')
    else:
        form = HistorialMedicoForm()
    return render(request, 'vacunas/crear_historial_medico.html', {'form': form})
