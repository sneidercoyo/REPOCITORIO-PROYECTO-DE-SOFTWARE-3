from django.db import models

class Propietario(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    direccion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=45, blank=True)

class Especie(models.Model):
    nombre = models.CharField(max_length=45)

class Mascota(models.Model):
    nombre = models.CharField(max_length=45)
    especie = models.ForeignKey(Especie, on_delete=models.RESTRICT)
    raza = models.CharField(max_length=45, blank=True)
    fecha_nacimiento = models.DateField()
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)

class Veterinario(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=45, blank=True)

class Vacuna(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Cita(models.Model):
    fecha = models.DateField()
    motivo = models.CharField(max_length=100)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True)

class HistorialMedico(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True)

class HistorialVacunas(models.Model):
    historial_medico = models.ForeignKey(HistorialMedico, on_delete=models.CASCADE)
    vacuna = models.ForeignKey(Vacuna, on_delete=models.CASCADE)
    fecha_aplicacion = models.DateField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('administrada', 'Administrada'), ('no administrada', 'No administrada')])
