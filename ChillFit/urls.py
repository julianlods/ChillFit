# ChillFit/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import perfil
from .views import get_plan_pago


urlpatterns = [
    # Ruta principal para "home"
    path('', views.home, name='home'),

    # Rutas de autenticación (personalizadas o genéricas)
    path('login/', auth_views.LoginView.as_view(template_name='ChillFit/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Rutas para otras funcionalidades
    path('register/', views.register_view, name='register'),
    path('rutinas/', views.ver_rutinas, name='ver_rutinas'),
    path('rutinas/<int:rutina_id>/', views.ver_rutina_detalle, name='ver_rutina_detalle'),
    path('rutinas/<int:rutina_id>/realizar/', views.marcar_rutina_realizada, name='marcar_rutina_realizada'),
    path('contacto/', views.contacto, name='contacto'),
    path('enviar_consulta/', views.enviar_consulta, name='enviar_consulta'),
    path('perfil/', perfil, name='perfil'),

    #Rutas de pagos con MercadoPago
    path('generar_pago/', views.generar_pago, name='generar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_fallido/', views.pago_fallido, name='pago_fallido'),
    path('admin/get_plan_pago/<int:user_id>/', get_plan_pago, name='get_plan_pago'),
    path('informar_transferencia/', views.informar_transferencia, name='informar_transferencia'),
]

