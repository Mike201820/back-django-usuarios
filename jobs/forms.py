from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Empresa, Postulante, Oferta, Aplicacion


class AplicacionForm(forms.ModelForm):
    class Meta:
        model = Aplicacion
        fields = ['oferta', 'postulante', 'estado_aplicacion']
        
class EmpresaRegisterForm(UserCreationForm):

    nombre = forms.CharField(max_length=255, required=True)
    direccion = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'nombre', 'direccion']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_empresa = True
        if commit:
            user.save()
            empresa = Empresa(user=user, nombre=self.cleaned_data['nombre'], direccion=self.cleaned_data['direccion'])
            empresa.save()
        return user

class PostulanteRegisterForm(UserCreationForm):

    nombre = forms.CharField(max_length=255, required=True)
    cv = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'nombre', 'cv']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_postulante = True
        if commit:
            user.save()
            postulante = Postulante(user=user, nombre=self.cleaned_data['nombre'], cv=self.cleaned_data['cv'])
            postulante.save()
        return user


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion']