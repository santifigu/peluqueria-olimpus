from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('reservar/', views.reservar, name='reservar'),
    path('confirmacion/<int:turno_id>/', views.confirmacion, name='confirmacion'),
]
