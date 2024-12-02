from django import forms
from .models import Propietario, Mascota, Vacunacion, Vacuna, HistorialVacuna, Especie, Cita, Veterinario

class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = '__all__'

class MascotaForm(forms.ModelForm):
    cedula_propietario = forms.CharField(max_length=45, required=True, label="Cédula del Propietario")

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento']

    def clean_cedula_propietario(self):
        cedula = self.cleaned_data.get('cedula_propietario')
        try:
            propietario = Propietario.objects.get(cedula=cedula)
        except Propietario.DoesNotExist:
            raise forms.ValidationError("No existe un propietario con esa cédula.")
        return propietario

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

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cedula_propietario', 'mascota', 'veterinario', 'fecha_hora', 'motivo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mascota'].queryset = Mascota.objects.none()

    def clean_cedula_propietario(self):
        cedula = self.cleaned_data.get('cedula_propietario')
        try:
            propietario = Propietario.objects.get(cedula=cedula)
            self.fields['mascota'].queryset = Mascota.objects.filter(propietario=propietario)
        except Propietario.DoesNotExist:
            raise forms.ValidationError("No existe un propietario con esa cédula.")
        return cedula
