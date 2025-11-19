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

    valor_euro = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="El valor de 1 EUR en VES",
        null=True,  # Importante: Permite nulos en la BD
        blank=True,  # Importante: Permite que esté vacío en el Admin
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
        # Actualizamos el 'str' para que muestre ambas monedas
        usd_str = f"USD: {self.valor}"

        # Mostramos el EUR solo si tiene un valor
        eur_str = f"EUR: {self.valor_euro}" if self.valor_euro else ""

        return f"Tasa del {self.fecha_vigencia} - {usd_str} | {eur_str}"
