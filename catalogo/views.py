from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Negocio, CategoriaServicio, Servicio
from .forms import MensajeContactoForm


def home(request):
    negocio = Negocio.objects.first()
    servicios_destacados = Servicio.objects.filter(activo=True)[:6]
    return render(request, 'catalogo/home.html', {
        'negocio': negocio,
        'servicios': servicios_destacados,
    })


def catalogo_servicios(request):
    negocio = Negocio.objects.first()
    categorias = CategoriaServicio.objects.prefetch_related('servicios').all()
    return render(request, 'catalogo/catalogo.html', {
        'negocio': negocio,
        'categorias': categorias,
    })


def contacto(request):
    negocio = Negocio.objects.first()
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Gracias! Te vamos a responder a la brevedad.")
            return redirect('catalogo:contacto')
    else:
        form = MensajeContactoForm()
    return render(request, 'catalogo/contacto.html', {'negocio': negocio, 'form': form})
