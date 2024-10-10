from django import forms
from .models import Mascota, Vacuna, Cita, HistorialMedico, Propietario, Especie

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'propietario']

class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'descripcion', 'precio']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'motivo', 'mascota', 'veterinario']

class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'email']

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nombre']
