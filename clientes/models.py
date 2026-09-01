from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from reservas.models import Turno


class ClientePerfil(models.Model):
    """Perfil de cliente recurrente (Plan Premium): historial y datos de contacto
    persistentes, sin necesidad de un sistema de cuentas/login completo."""
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    notas_internas = models.TextField(blank=True, help_text="Solo visible para el equipo del salón")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Perfil de cliente"
        verbose_name_plural = "Perfiles de clientes"

    def __str__(self):
        return self.nombre

    @property
    def cantidad_visitas(self):
        return Turno.objects.filter(email_cliente=self.email, estado='completado').count()


class Resena(models.Model):
    """Reseña dejada por un cliente sobre un turno ya completado."""
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE, related_name='resena')
    puntaje = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    publicada = models.BooleanField(default=False, help_text="Solo las reseñas publicadas se muestran en el sitio")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"{self.turno.nombre_cliente} - {self.puntaje}★"


class Pago(models.Model):
    """Registro de pago/seña vía Mercado Pago para un turno (Plan Premium)."""
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('reembolsado', 'Reembolsado'),
    ]
    turno = models.OneToOneField(Turno, on_delete=models.CASCADE, related_name='pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    es_sena = models.BooleanField(default=True, help_text="Si es False, se cobró el servicio completo")
    mercadopago_payment_id = models.CharField(max_length=100, blank=True)
    mercadopago_preference_id = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago #{self.id} - {self.turno} - {self.get_estado_display()}"
