from django.db import models
from django.utils import timezone


class TasaCambio(models.Model):
    """
    Modelo para almacenar la tasa de cambio diaria de USD a VES.
    """

    # Usamos DecimalField para precisión monetaria.
    # max_digits = Número total de dígitos.
    # decimal_places = Cuántos de esos son decimales.
    # (Ej: 123456.78)
    valor = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="El valor de 1 USD en VES"
    )

    # Fecha en que esta tasa entra en vigencia.
    # Usamos default=timezone.now para que tome la fecha actual
    # al crearla en el admin, pero se puede cambiar.
    fecha_vigencia = models.DateField(
        default=timezone.now,
        unique=True,  # Solo puede haber una tasa por día.
        help_text="Fecha de vigencia de la tasa",
    )

    class Meta:
        # Esto es importante: le decimos a Django que,
        # cuando busquemos tasas, las ordene por fecha
        # (la más nueva primero).
        ordering = ["-fecha_vigencia"]

    def __str__(self):
        # Esto es para que en el panel de admin se vea
        # "Tasa del [fecha]: [valor]" en lugar de "TasaCambio object (1)"
        return f"Tasa del {self.fecha_vigencia}: {self.valor} VES"
