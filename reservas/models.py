from django.db import models
from django.core.exceptions import ValidationError
from catalogo.models import Servicio


class Profesional(models.Model):
    """Peluquero/a que atiende turnos."""
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='profesionales/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"

    def __str__(self):
        return self.nombre


class HorarioAtencion(models.Model):
    """Franjas horarias en las que se puede reservar, por día de semana."""
    DIAS = [
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'),
        (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo'),
    ]
    dia_semana = models.IntegerField(choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ['dia_semana', 'hora_inicio']
        verbose_name = "Horario de atención"
        verbose_name_plural = "Horarios de atención"

    def __str__(self):
        return f"{self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class Turno(models.Model):
    """Un turno reservado por un cliente (Plan Intermedio)."""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('completado', 'Completado'),
    ]
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name='turnos')
    profesional = models.ForeignKey(Profesional, on_delete=models.SET_NULL, null=True, blank=True, related_name='turnos')
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=30)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    recordatorio_enviado = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        constraints = [
            models.UniqueConstraint(
                fields=['profesional', 'fecha', 'hora'],
                condition=models.Q(estado__in=['pendiente', 'confirmado']),
                name='turno_unico_por_profesional_horario',
            )
        ]

    def __str__(self):
        return f"{self.nombre_cliente} - {self.servicio} - {self.fecha} {self.hora}"
