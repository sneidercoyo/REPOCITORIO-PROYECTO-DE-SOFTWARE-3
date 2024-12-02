from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Propietario, Mascota, Vacunacion, Vacuna, HistorialVacuna, Especie, Cita, Veterinario
from .forms import PropietarioForm, MascotaForm, BusquedaForm, VacunaForm, EspecieForm, CitaForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from datetime import datetime
import time

def inicio(request):
    return render(request, 'vacunacion/inicio.html')

def registrar_propietario(request):
    form = PropietarioForm()
    mensaje = None

    if request.method == 'POST':
        form = PropietarioForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "El propietario ha sido registrado con éxito."

    return render(request, 'vacunacion/registrar_propietario.html', {
        'form': form,
        'mensaje': mensaje
    })

def registrar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'mensaje': 'Cita registrada correctamente. Redirigiendo...',
                    'redirect': True
                })
            return redirect('servicios')
    else:
        form = CitaForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cedula = request.GET.get('cedula_propietario')
        try:
            propietario = Propietario.objects.get(cedula=cedula)
            mascotas = Mascota.objects.filter(propietario=propietario).values('id', 'nombre')
            return JsonResponse(list(mascotas), safe=False)
        except Propietario.DoesNotExist:
            return JsonResponse([], safe=False)

    return render(request, 'vacunacion/registrar_cita.html', {'form': form})



def registrar_mascota(request):
    mensaje = None
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            propietario = form.cleaned_data['cedula_propietario']
            mascota.propietario = propietario
            mascota.save()
            mensaje = "La mascota ha sido registrada exitosamente."
            return redirect('servicios')
    else:
        form = MascotaForm()

    return render(request, 'vacunacion/registrar_mascota.html', {'form': form, 'mensaje': mensaje})

def registrar_especie(request):
    if request.method == 'POST':
        form = EspecieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = EspecieForm()
    return render(request, 'vacunacion/registrar_especie.html', {'form': form})

def registrar_vacuna(request):
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = VacunaForm()
    return render(request, 'vacunacion/registrar_vacuna.html', {'form': form})

def buscar_mascota(request):
    mascota = None
    propietario = None
    if request.method == 'GET':
        form = BusquedaForm(request.GET)
        if form.is_valid():
            id_mascota = form.cleaned_data.get('id_mascota')
            cedula_propietario = form.cleaned_data.get('cedula')

            if id_mascota:
                mascota = get_object_or_404(Mascota, id=id_mascota)
                propietario = mascota.propietario

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

def consultar_carnet(request):
    mascotas = None
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        if cedula:
            try:
                propietario = Propietario.objects.get(cedula=cedula)
                mascotas = Mascota.objects.filter(propietario=propietario)
            except Propietario.DoesNotExist:
                mascotas = None
    return render(request, 'vacunacion/consultar_carnet.html', {'mascotas': mascotas})

def carnet_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    historial_vacunas = HistorialVacuna.objects.filter(mascota=mascota).order_by('-fecha_aplicacion')
    
    for vacuna in historial_vacunas:
        vacuna.dias_restantes = vacuna.dias_hasta_proxima()

    return render(request, 'vacunacion/carnet_mascota.html', {
        'mascota': mascota,
        'historial_vacunas': historial_vacunas,
        'cedula_propietario': mascota.propietario.cedula
    })

def descargar_carnet_pdf(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    historial_vacunas = HistorialVacuna.objects.filter(mascota=mascota).order_by('-fecha_aplicacion')

    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        fontSize=18,
        textColor=colors.HexColor("#007BFF"),
        fontName="Helvetica-Bold",
        alignment=1
    )
    date_style = ParagraphStyle(
        'Date',
        fontSize=10,
        textColor=colors.HexColor("#666666"),
        fontName="Helvetica",
        alignment=2
    )

    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
    logo = Image(logo_path, width=50, height=50)

    title = Paragraph(f"Carnet de Vacunación de {mascota.nombre}", title_style)
    header = Table([[logo, title]], colWidths=[50, 400])
    header.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))

    date = Paragraph(f"Fecha de impresión: {fecha_actual}", date_style)

    elements = [Spacer(1, 20), date, Spacer(1, 10), header, Spacer(1, 20)]

    info_data = [
        ['Especie', mascota.especie],
        ['Raza', mascota.raza],
        ['Fecha de Nacimiento', mascota.fecha_nacimiento.strftime('%Y-%m-%d')],
        ['Propietario', mascota.propietario],['Propietario', mascota.propietario],
        ['Cédula del Propietario', mascota.propietario.cedula]
    ]
    info_table = Table(info_data, colWidths=[150, 350])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f8f9fa")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#333333")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 24))

    header = ['Vacuna', 'Fecha de Aplicación', 'Estado', 'Próxima Vacuna', 'Notas']
    data = [header]
    for vacuna in historial_vacunas:
        proxima = f"{vacuna.fecha_proxima} (en {vacuna.dias_hasta_proxima()} días)" if vacuna.fecha_proxima else "No programada"
        data.append([
            vacuna.vacuna.nombre,
            str(vacuna.fecha_aplicacion),
            vacuna.get_estado_display(),
            proxima,
            vacuna.notas or "Sin notas"
        ])

    table = Table(data, colWidths=[120, 100, 100, 120, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007BFF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#333333")),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')

def servicios(request):
    return render(request, 'vacunacion/servicios.html')

def nosotros(request):
    return render(request, 'vacunacion/nosotros.html')

def clientes(request):
    return render(request, 'vacunacion/clientes.html')

