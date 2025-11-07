from django.contrib import admin
from .models import (
    Usuario, Categoria, Gasto, Ingreso,
    TipoLogro, LogroUsuario, MetaAhorro
)

# ==========================
# USUARIO PERSONALIZADO
# ==========================
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('nombre', 'correo')
    ordering = ('id',)


# ==========================
# CATEGORÍAS
# ==========================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria')
    search_fields = ('categoria',)


# ==========================
# GASTOS
# ==========================
@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'monto', 'forma_pago', 'fecha', 'categoria')
    list_filter = ('forma_pago', 'fecha', 'categoria')
    search_fields = ('usuario__nombre', 'nota')
    autocomplete_fields = ['usuario', 'categoria']


# ==========================
# INGRESOS
# ==========================
@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'monto', 'forma_pago', 'fecha')
    search_fields = ('usuario__nombre',)
    autocomplete_fields = ['usuario']


# ==========================
# TIPOS DE LOGROS
# ==========================
@admin.register(TipoLogro)
class TipoLogroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'meta', 'color', 'icono')
    search_fields = ('nombre', 'tipo')
    list_filter = ('tipo',)


# ==========================
# LOGROS DE USUARIO
# ==========================
@admin.register(LogroUsuario)
class LogroUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo_logro', 'progreso_actual', 'completado', 'fecha_completado')
    list_filter = ('completado',)
    search_fields = ('usuario__nombre', 'tipo_logro__nombre')
    autocomplete_fields = ['usuario', 'tipo_logro']


# ==========================
# METAS DE AHORRO
# ==========================
@admin.register(MetaAhorro)
class MetaAhorroAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nombre_meta', 'meta_total', 'monto_actual', 'estado', 'icono', 'fecha_objetivo')
    list_filter = ('estado',)
    search_fields = ('nombre_meta', 'usuario__nombre')
    autocomplete_fields = ['usuario']
