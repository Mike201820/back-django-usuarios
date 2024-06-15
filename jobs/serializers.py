from rest_framework import serializers
from .models import Empresa, Postulante, Oferta, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_empresa', 'is_postulante']

class EmpresaSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Empresa
        fields = '__all__'

class PostulanteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Postulante
        fields = '__all__'

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'
