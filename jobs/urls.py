from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, register_empresa, register_postulante, crear_oferta, ofertas_lista, postularse_a_oferta, mis_postulaciones,CustomLoginView, CustomLogoutView, edit_offer, delete_offer, apply_for_offer, list_applications, view_applications, update_application_status, view_accepted_applications, CustomUserViewSet, EmpresaViewSet, PostulanteViewSet, OfertaViewSet, AplicacionViewSet, generate_applications_report,generate_statistics_report


router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'postulantes', PostulanteViewSet)
router.register(r'ofertas', OfertaViewSet)
router.register(r'aplicaciones', AplicacionViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    
    path('register/empresa/', register_empresa, name='register-empresa'),
    path('register/postulante/', register_postulante, name='register-postulante'),
    path('ofertas/', ofertas_lista, name='ofertas_lista'),
    path('crear_oferta/', crear_oferta, name='crear_oferta'),
    path('postularse/<int:oferta_id>/', postularse_a_oferta, name='postularse_a_oferta'),  # Ruta para postularse
    path('mis_postulaciones/', mis_postulaciones, name='mis_postulaciones'),
    path('offer/edit/<int:offer_id>/', edit_offer, name='edit-offer'),
    path('offer/delete/<int:offer_id>/', delete_offer, name='delete-offer'),
    path('offer/apply/<int:offer_id>/', apply_for_offer, name='apply-for-offer'),
    path('applications/', list_applications, name='list-applications'),
    path('applications/view/', view_applications, name='view-applications'),
    path('application/update/<int:application_id>/', update_application_status, name='update-application-status'),
    path('applications/accepted/', view_accepted_applications, name='view-accepted-applications'),
    path('reportes/aplicaciones/', generate_applications_report, name='reporte_aplicaciones'),
    path('reportes/estadisticas/', generate_statistics_report, name='reporte_estadisticas'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
