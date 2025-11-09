from rest_framework import serializers
from .models import TasaCambio


class TasaCambioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TasaCambio.
    Convierte el modelo TasaCambio a formato JSON.
    """

    class Meta:
        model = TasaCambio

        # Le decimos qué campos del modelo queremos exponer
        # en nuestra API.
        fields = ["valor", "fecha_vigencia"]
