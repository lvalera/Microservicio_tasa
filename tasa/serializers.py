from rest_framework import serializers
from .models import TasaCambio


class TasaCambioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TasaCambio.
    """

    class Meta:
        model = TasaCambio

        # Añadimos 'valor_euro' a la lista de campos a exponer
        fields = ["valor", "valor_euro", "fecha_vigencia"]
