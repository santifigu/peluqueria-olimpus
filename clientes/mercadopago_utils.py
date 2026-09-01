"""Integración con Mercado Pago (Plan Premium).

Requiere en settings.py:
    MERCADOPAGO_ACCESS_TOKEN = "APP_USR-..."  # token del vendedor
    SITE_URL = "https://tu-dominio.com"        # para las URLs de retorno
"""
import mercadopago
from django.conf import settings


def _sdk():
    return mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)


def crear_preferencia(turno, monto, es_sena=True):
    """Crea una preferencia de pago para un turno y devuelve (init_point, preference_id)."""
    sdk = _sdk()
    concepto = "Seña" if es_sena else "Pago"
    preference_data = {
        "items": [{
            "title": f"{concepto} - {turno.servicio.nombre}",
            "quantity": 1,
            "unit_price": float(monto),
            "currency_id": "ARS",
        }],
        "payer": {
            "name": turno.nombre_cliente,
            "email": turno.email_cliente,
        },
        "external_reference": str(turno.id),
        "back_urls": {
            "success": f"{settings.SITE_URL}/reservas/confirmacion/{turno.id}/",
            "failure": f"{settings.SITE_URL}/reservas/reservar/",
            "pending": f"{settings.SITE_URL}/reservas/confirmacion/{turno.id}/",
        },
        "notification_url": f"{settings.SITE_URL}/clientes/webhook/mercadopago/",
        "auto_return": "approved",
    }
    resultado = sdk.preference().create(preference_data)
    preferencia = resultado["response"]
    return preferencia["init_point"], preferencia["id"]


def consultar_pago(payment_id):
    """Consulta el estado de un pago por su ID (usado desde el webhook)."""
    sdk = _sdk()
    resultado = sdk.payment().get(payment_id)
    return resultado["response"]
