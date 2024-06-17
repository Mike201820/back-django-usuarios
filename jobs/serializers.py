from rest_framework import serializers
from .models import CustomUser, Empresa, Postulante, Oferta, Aplicacion

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_empresa', 'is_postulante']

class EmpresaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Empresa
        fields = ['id', 'user', 'nombre', 'direccion']

class PostulanteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Postulante
        fields = ['id', 'user', 'nombre', 'cv']

class OfertaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    postulantes = PostulanteSerializer(many=True, read_only=True)

    class Meta:
        model = Oferta
        fields = ['id', 'empresa', 'titulo', 'descripcion', 'fecha_publicacion', 'postulantes']

class AplicacionSerializer(serializers.ModelSerializer):
    oferta = OfertaSerializer()
    postulante = PostulanteSerializer()

    class Meta:
        model = Aplicacion
        fields = ['id', 'oferta', 'postulante', 'fecha_aplicacion', 'estado_aplicacion']
