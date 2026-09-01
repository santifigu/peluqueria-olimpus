from django.contrib import admin
from .models import Profesional, HorarioAtencion, Turno


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')


@admin.register(HorarioAtencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'hora_inicio', 'hora_fin')


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'servicio', 'profesional', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'profesional')
    search_fields = ('nombre_cliente', 'email_cliente')
    date_hierarchy = 'fecha'
