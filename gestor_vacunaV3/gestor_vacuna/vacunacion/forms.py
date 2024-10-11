from django import forms
from .models import Propietario, Mascota, Especie, Vacuna

class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = '__all__'

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'

class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = '__all__'

class BusquedaForm(forms.Form):
    cedula = forms.CharField(max_length=11, required=False, label='Cédula del propietario')
    id_mascota = forms.IntegerField(required=False, label='ID de la mascota')

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = '__all__'
