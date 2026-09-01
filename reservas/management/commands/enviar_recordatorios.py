"""
Envía recordatorios de turno a los clientes que tienen un turno mañana.
Plan Premium. Pensado para correrse una vez al día vía cron:

    0 9 * * * /ruta/al/venv/bin/python manage.py enviar_recordatorios

o como tarea periódica de Celery Beat si el proyecto ya usa Celery.
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from reservas.models import Turno


class Command(BaseCommand):
    help = "Envía recordatorios por email a los turnos de mañana que no fueron notificados"

    def handle(self, *args, **options):
        manana = timezone.localdate() + timedelta(days=1)
        turnos = Turno.objects.filter(
            fecha=manana,
            estado__in=['pendiente', 'confirmado'],
            recordatorio_enviado=False,
        )

        enviados = 0
        for turno in turnos:
            send_mail(
                subject="Recordatorio de tu turno de mañana",
                message=(
                    f"Hola {turno.nombre_cliente}, te recordamos tu turno para "
                    f"{turno.servicio.nombre} mañana {turno.fecha.strftime('%d/%m')} "
                    f"a las {turno.hora.strftime('%H:%M')}."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[turno.email_cliente],
                fail_silently=True,
            )
            turno.recordatorio_enviado = True
            turno.save(update_fields=['recordatorio_enviado'])
            enviados += 1

        self.stdout.write(self.style.SUCCESS(f"Recordatorios enviados: {enviados}"))
