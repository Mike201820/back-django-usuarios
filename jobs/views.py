from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmpresa, IsPostulante
from rest_framework import generics,viewsets
from .models import CustomUser, Empresa, Postulante, Oferta,Aplicacion
from .serializers import CustomUserSerializer, EmpresaSerializer, PostulanteSerializer, OfertaSerializer, AplicacionSerializer
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmpresaRegisterForm, PostulanteRegisterForm,OfertaForm,AplicacionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
from django.core.files.temp import NamedTemporaryFile
from reportlab.lib.utils import ImageReader
from tempfile import NamedTemporaryFile

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/login'

#def index(request):
    #ofertas = Oferta.objects.all()
    #return render(request, 'index.html', {'ofertas': ofertas})
@never_cache
@login_required
def index(request):
    if request.user.is_empresa:
        empresa = Empresa.objects.get(user=request.user)
        ofertas = Oferta.objects.filter(empresa=empresa)
    else:
        ofertas = Oferta.objects.all()
    return render(request, 'index.html', {'ofertas': ofertas})


def register_empresa(request):
    if request.method == 'POST':
        form = EmpresaRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = EmpresaRegisterForm()
    return render(request, 'register.html', {'form': form, 'user_type': 'Empresa'})

def register_postulante(request):
    if request.method == 'POST':
        form = PostulanteRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = PostulanteRegisterForm()
    return render(request, 'register.html', {'form': form, 'user_type': 'Postulante'})


@login_required
def crear_oferta(request):
    if request.user.is_empresa:
        empresa = Empresa.objects.get(user=request.user)
        if request.method == 'POST':
            form = OfertaForm(request.POST)
            if form.is_valid():
                oferta = form.save(commit=False)
                oferta.empresa = empresa
                oferta.save()
                return redirect('index')  # Redirige a la lista de ofertas o a donde prefieras
        else:
            form = OfertaForm()
        return render(request, 'crear_oferta.html', {'form': form})
    else:
        return redirect('index') 


def ofertas_lista(request):
    ofertas = Oferta.objects.all()
    return render(request, 'ofertas_lista.html', {'ofertas': ofertas})


@login_required
def edit_offer(request, offer_id):
    offer = get_object_or_404(Oferta, id=offer_id, empresa=request.user.empresa)
    if request.method == 'POST':
        form = OfertaForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OfertaForm(instance=offer)
    return render(request, 'edit_offer.html', {'form': form})

@login_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(Oferta, id=offer_id, empresa=request.user.empresa)
    if request.method == 'POST':
        offer.delete()
        return redirect('index')
    return render(request, 'delete_offer.html', {'offer': offer})


@login_required
def apply_for_offer(request, offer_id):
    oferta = get_object_or_404(Oferta, id=offer_id)
    postulante = request.user.postulante

    if request.method == 'POST':
        Aplicacion.objects.create(
            oferta=oferta,
            postulante=postulante,
            estado_aplicacion='Pendiente'
        )
        return redirect('index')

    return render(request, 'apply_for_offer.html', {'oferta': oferta})

@login_required
def list_applications(request):
    postulante = request.user.postulante
    aplicaciones = Aplicacion.objects.filter(postulante=postulante)
    return render(request, 'list_applications.html', {'aplicaciones': aplicaciones})



@login_required
def postularse_a_oferta(request, oferta_id):
    if request.user.is_postulante:
        oferta = get_object_or_404(Oferta, id=oferta_id)
        postulante = Postulante.objects.get(user=request.user)
        if postulante not in oferta.postulantes.all():
            oferta.postulantes.add(postulante)
            messages.success(request, 'Te has postulado exitosamente a la oferta.')
        else:
            messages.warning(request, 'Ya te has postulado a esta oferta.')
        return redirect('index')
    else:
        return redirect('index')
    

@login_required
def mis_postulaciones(request):
    if request.user.is_postulante:
        postulante = Postulante.objects.get(user=request.user)
        ofertas = postulante.ofertas.all()
        return render(request, 'mis_postulaciones.html', {'ofertas': ofertas})
    else:
        return redirect('index')


@login_required
def view_applications(request):
    if not hasattr(request.user, 'empresa'):
        return HttpResponseForbidden("No tienes permiso para ver esta página.")

    empresa = request.user.empresa
    ofertas = Oferta.objects.filter(empresa=empresa)
    aplicaciones = Aplicacion.objects.filter(oferta__in=ofertas)

    return render(request, 'view_applications.html', {'aplicaciones': aplicaciones})


@login_required
@require_POST
def update_application_status(request, application_id):
    if not hasattr(request.user, 'empresa'):
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    aplicacion = get_object_or_404(Aplicacion, id=application_id)
    if aplicacion.oferta.empresa != request.user.empresa:
        return HttpResponseForbidden("No tienes permiso para actualizar esta aplicación.")

    estado = request.POST.get('estado_aplicacion')
    if estado in ['Pendiente', 'Aceptada', 'Rechazada']:
        aplicacion.estado_aplicacion = estado
        aplicacion.save()

    return redirect('view-applications')


@login_required
def view_accepted_applications(request):
    if not hasattr(request.user, 'postulante'):
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    postulante = request.user.postulante
    aplicaciones = Aplicacion.objects.filter(postulante=postulante, estado_aplicacion='Aceptada')

    return render(request, 'view_accepted_applications.html', {'aplicaciones': aplicaciones})


@login_required
def generate_applications_report(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")

    # Crear un objeto HttpResponse con un encabezado PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_aplicaciones.pdf"'

    # Crear un objeto Canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título del reporte
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, "Reporte de Aplicaciones")
    y -= 30

    # Obtener datos de aplicaciones
    aplicaciones = Aplicacion.objects.all()

    for aplicacion in aplicaciones:
        oferta = aplicacion.oferta
        postulante = aplicacion.postulante
        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"Oferta: {oferta.titulo}")
        y -= 20
        p.drawString(120, y, f"Postulante: {postulante.nombre}")
        y -= 20
        p.drawString(120, y, f"Estado: {aplicacion.estado_aplicacion}")
        y -= 30

        if y < 150:  # Nueva página si el contenido es demasiado largo
            p.showPage()
            y = height - 50

    # Generar gráfico de aplicaciones por estado
    estados = [estado for estado, _ in Aplicacion.ESTADO_CHOICES]
    counts = [Aplicacion.objects.filter(estado_aplicacion=estado).count() for estado in estados]

    fig, ax = plt.subplots()
    ax.bar(estados, counts)
    ax.set_xlabel('Estado')
    ax.set_ylabel('Cantidad')
    ax.set_title('Distribución de Aplicaciones por Estado')

    # Guardar el gráfico en un archivo temporal
    with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.savefig(tmpfile.name)
        tmpfile.seek(0)
        p.drawImage(ImageReader(tmpfile), 100, y - 150, width=400, height=150)
        tmpfile.close()

    p.showPage()
    p.save()
    return response


@login_required
def generate_statistics_report(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")

    # Crear un objeto HttpResponse con un encabezado PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_estadisticas.pdf"'

    # Crear un objeto Canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título del reporte
    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, "Reporte de Estadísticas")
    y -= 30

    # Obtener estadísticas
    num_ofertas = Oferta.objects.count()
    num_aplicaciones = Aplicacion.objects.count()
    num_empresas = Empresa.objects.count()
    num_postulantes = Postulante.objects.count()

    # Añadir estadísticas al PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Número de Ofertas: {num_ofertas}")
    y -= 20
    p.drawString(100, y, f"Número de Aplicaciones: {num_aplicaciones}")
    y -= 20
    p.drawString(100, y, f"Número de Empresas: {num_empresas}")
    y -= 20
    p.drawString(100, y, f"Número de Postulantes: {num_postulantes}")
    y -= 30

    # Distribución de aplicaciones por estado
    p.drawString(100, y, "Distribución de Aplicaciones por Estado:")
    y -= 20
    for estado, _ in Aplicacion.ESTADO_CHOICES:
        count = Aplicacion.objects.filter(estado_aplicacion=estado).count()
        p.drawString(120, y, f"{estado}: {count}")
        y -= 20

    # Generar gráfico de distribución de aplicaciones por estado
    estados = [estado for estado, _ in Aplicacion.ESTADO_CHOICES]
    counts = [Aplicacion.objects.filter(estado_aplicacion=estado).count() for estado in estados]

    fig, ax = plt.subplots()
    ax.bar(estados, counts)
    ax.set_xlabel('Estado')
    ax.set_ylabel('Cantidad')
    ax.set_title('Distribución de Aplicaciones por Estado')

    # Guardar el gráfico en un archivo temporal
    with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        fig.savefig(tmpfile.name)
        tmpfile.seek(0)
        p.drawImage(ImageReader(tmpfile), 100, y - 200, width=400, height=150)
        tmpfile.close()

    p.showPage()
    p.save()
    return response


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class PostulanteViewSet(viewsets.ModelViewSet):
    queryset = Postulante.objects.all()
    serializer_class = PostulanteSerializer

class OfertaViewSet(viewsets.ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer

class AplicacionViewSet(viewsets.ModelViewSet):
    queryset = Aplicacion.objects.all()
    serializer_class = AplicacionSerializer