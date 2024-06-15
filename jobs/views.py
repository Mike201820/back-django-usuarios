from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmpresa, IsPostulante
from rest_framework import generics
from .models import Empresa, Postulante, Oferta
from .serializers import EmpresaSerializer, PostulanteSerializer, OfertaSerializer
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmpresaRegisterForm, PostulanteRegisterForm


def index(request):
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




class EmpresaListCreate(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated, IsEmpresa]

class PostulanteListCreate(generics.ListCreateAPIView):
    queryset = Postulante.objects.all()
    serializer_class = PostulanteSerializer
    permission_classes = [IsAuthenticated, IsPostulante]

class OfertaListCreate(generics.ListCreateAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
    permission_classes = [IsAuthenticated, IsEmpresa]

class OfertaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
    permission_classes = [IsAuthenticated, IsEmpresa]
