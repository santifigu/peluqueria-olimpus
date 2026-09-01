from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Turno
from .forms import TurnoForm
from catalogo.models import Negocio


def reservar(request):
    negocio = Negocio.objects.first()
    servicio_id = request.GET.get('servicio')
    initial = {'servicio': servicio_id} if servicio_id else {}

    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save()
            _enviar_confirmacion(turno)
            messages.success(request, "¡Turno reservado! Te enviamos la confirmación por email.")
            return redirect('reservas:confirmacion', turno_id=turno.id)
    else:
        form = TurnoForm(initial=initial)

    return render(request, 'reservas/reservar.html', {'form': form, 'negocio': negocio})


def confirmacion(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    return render(request, 'reservas/confirmacion.html', {'turno': turno})


def _enviar_confirmacion(turno):
    """Envía el email de confirmación. En dev usar EMAIL_BACKEND de consola."""
    try:
        send_mail(
            subject=f"Confirmación de turno - {turno.servicio.nombre}",
            message=(
                f"Hola {turno.nombre_cliente},\n\n"
                f"Tu turno para {turno.servicio.nombre} quedó reservado para "
                f"el {turno.fecha.strftime('%d/%m/%Y')} a las {turno.hora.strftime('%H:%M')}.\n\n"
                "¡Te esperamos!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[turno.email_cliente],
            fail_silently=True,
        )
    except Exception:
        pass
