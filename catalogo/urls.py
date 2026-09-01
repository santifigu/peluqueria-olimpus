from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.home, name='home'),
    path('servicios/', views.catalogo_servicios, name='catalogo'),
    path('contacto/', views.contacto, name='contacto'),
]
