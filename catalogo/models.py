from django.db import models


class Negocio(models.Model):
    """Datos generales de la peluquería (Plan Básico). Pensado como singleton:
    se espera un único registro con la info del local."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=30, blank=True, help_text="Número con código de país, ej: 5493511234567")
    instagram = models.URLField(blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    logo = models.ImageField(upload_to='negocio/', blank=True, null=True)

    class Meta:
        verbose_name = "Datos del negocio"
        verbose_name_plural = "Datos del negocio"

    def __str__(self):
        return self.nombre


class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=80)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """Un servicio del catálogo (corte, color, tratamiento, etc.)."""
    categoria = models.ForeignKey(CategoriaServicio, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(help_text="Duración estimada en minutos")
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['categoria__orden', 'nombre']
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"{self.nombre} (${self.precio})"


class MensajeContacto(models.Model):
    """Formulario de contacto simple del Plan Básico."""
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"{self.nombre} - {self.creado:%d/%m/%Y}"
