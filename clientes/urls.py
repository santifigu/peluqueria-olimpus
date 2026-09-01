from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('pagar-sena/<int:turno_id>/', views.pagar_sena, name='pagar_sena'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    path('resena/<int:turno_id>/', views.dejar_resena, name='dejar_resena'),
    path('resenas/', views.resenas_publicas, name='resenas_publicas'),
]
