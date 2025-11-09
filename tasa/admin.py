from django.contrib import admin
from .models import TasaCambio

# Usamos un decorador (@admin.register) para registrar el modelo.
# Esto nos permite personalizar cómo se ve en el admin.


@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo TasaCambio en el admin.
    """

    # Muestra estas columnas en la lista de tasas
    list_display = ("fecha_vigencia", "valor")

    # Añade un filtro lateral para navegar por fechas
    list_filter = ("fecha_vigencia",)

    # Asegura el orden (aunque ya está en el Meta del modelo)
    ordering = ("-fecha_vigencia",)
