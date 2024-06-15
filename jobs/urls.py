from django.urls import path
from .views import EmpresaListCreate, PostulanteListCreate, OfertaListCreate, OfertaDetail, index, register_empresa, register_postulante

urlpatterns = [
    path('', index, name='index'),
    path('empresas/', EmpresaListCreate.as_view(), name='empresa-list-create'),
    path('postulantes/', PostulanteListCreate.as_view(), name='postulante-list-create'),
    path('ofertas/', OfertaListCreate.as_view(), name='oferta-list-create'),
    path('ofertas/<int:pk>/', OfertaDetail.as_view(), name='oferta-detail'),
    path('register/empresa/', register_empresa, name='register-empresa'),
    path('register/postulante/', register_postulante, name='register-postulante'),
]
