import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from reservas.models import Turno
from .models import Pago, Resena
from .mercadopago_utils import crear_preferencia, consultar_pago
from .forms import ResenaForm


def pagar_sena(request, turno_id):
    """Genera el link de pago de Mercado Pago para la seña del turno."""
    turno = get_object_or_404(Turno, id=turno_id)
    monto_sena = turno.servicio.precio * Decimal('0.30')  # 30% de seña por defecto

    pago, _ = Pago.objects.get_or_create(
        turno=turno,
        defaults={'monto': monto_sena, 'es_sena': True},
    )
    init_point, preference_id = crear_preferencia(turno, monto_sena, es_sena=True)
    pago.mercadopago_preference_id = preference_id
    pago.save(update_fields=['mercadopago_preference_id'])

    return redirect(init_point)


@csrf_exempt
def webhook_mercadopago(request):
    """Recibe notificaciones IPN/webhook de Mercado Pago y actualiza el pago."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    payment_id = request.GET.get('data.id') or request.GET.get('id')
    if not payment_id:
        try:
            body = json.loads(request.body or '{}')
            payment_id = body.get('data', {}).get('id')
        except json.JSONDecodeError:
            payment_id = None

    if payment_id:
        info_pago = consultar_pago(payment_id)
        turno_id = info_pago.get('external_reference')
        estado_mp = info_pago.get('status')  # approved, pending, rejected, refunded

        mapa_estados = {
            'approved': 'aprobado', 'pending': 'pendiente',
            'rejected': 'rechazado', 'refunded': 'reembolsado',
        }
        try:
            pago = Pago.objects.get(turno_id=turno_id)
            pago.mercadopago_payment_id = str(payment_id)
            pago.estado = mapa_estados.get(estado_mp, pago.estado)
            pago.save()
            if pago.estado == 'aprobado':
                pago.turno.estado = 'confirmado'
                pago.turno.save(update_fields=['estado'])
        except Pago.DoesNotExist:
            pass

    return HttpResponse(status=200)


def dejar_resena(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id, estado='completado')
    if hasattr(turno, 'resena'):
        messages.info(request, "Ya dejaste una reseña para este turno.")
        return redirect('catalogo:home')

    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.turno = turno
            resena.save()
            messages.success(request, "¡Gracias por tu reseña!")
            return redirect('catalogo:home')
    else:
        form = ResenaForm()
    return render(request, 'clientes/resena.html', {'form': form, 'turno': turno})


def resenas_publicas(request):
    resenas = Resena.objects.filter(publicada=True).select_related('turno')
    return render(request, 'clientes/resenas.html', {'resenas': resenas})


from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils import timezone
from reservas.models import Turno


@staff_member_required
def panel(request):
    """Panel a medida del Plan Premium: resumen operativo del día a día,
    pensado para que el dueño del salón lo mire sin entrar al admin de Django."""
    hoy = timezone.localdate()

    turnos_hoy = Turno.objects.filter(fecha=hoy).exclude(estado='cancelado').select_related('servicio', 'profesional')

    ingresos_mes = Pago.objects.filter(
        estado='aprobado', creado__year=hoy.year, creado__month=hoy.month
    ).aggregate(total=Sum('monto'))['total'] or 0

    servicios_top = (
        Turno.objects.filter(estado='completado')
        .values('servicio__nombre')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')[:5]
    )

    resenas_pendientes = Resena.objects.filter(publicada=False).count()

    return render(request, 'clientes/panel.html', {
        'turnos_hoy': turnos_hoy,
        'ingresos_mes': ingresos_mes,
        'servicios_top': servicios_top,
        'resenas_pendientes': resenas_pendientes,
    })
