from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TasaCambio
from .serializers import TasaCambioSerializer


class TasaVigenteView(APIView):
    """
    Endpoint de solo lectura que devuelve la tasa de cambio más reciente (vigente).
    """

    def get(self, request, format=None):
        """
        Maneja la petición GET.
        """
        # 1. Buscamos el objeto
        # Usamos .first() porque definimos el 'ordering'
        # en el Meta del modelo (recuerdas? '-fecha_vigencia').
        # Así que .first() siempre será el más nuevo.
        tasa = TasaCambio.objects.first()

        # 2. Validamos si existe
        if tasa is None:
            # Si no hay ninguna tasa en la BD, devolvemos un error 404
            return Response(
                {"error": "No hay tasas de cambio registradas."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 3. Serializamos (Traducimos)
        # Si encontramos la tasa, usamos el serializer que creamos.
        serializer = TasaCambioSerializer(tasa)

        # 4. Respondemos
        # Devolvemos los datos del serializer en formato JSON.
        return Response(serializer.data, status=status.HTTP_200_OK)
