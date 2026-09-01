from django.contrib import admin
from .models import ClientePerfil, Resena, Pago


@admin.register(ClientePerfil)
class ClientePerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'cantidad_visitas')
    search_fields = ('nombre', 'email')


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('turno', 'puntaje', 'publicada', 'creado')
    list_filter = ('publicada', 'puntaje')
    actions = ['publicar_resenas']

    @admin.action(description="Publicar reseñas seleccionadas")
    def publicar_resenas(self, request, queryset):
        queryset.update(publicada=True)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('turno', 'monto', 'es_sena', 'estado', 'creado')
    list_filter = ('estado', 'es_sena')
