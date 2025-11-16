import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import datetime

from django.core.management.base import BaseCommand
from tasa.models import TasaCambio

# URL oficial del BCV
URL_BCV = "https://www.bcv.org.ve/"

# Es una buena práctica simular ser un navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


class Command(BaseCommand):
    """
    Comando para extraer la tasa de cambio USD del BCV y guardarla
    en la base de datos.
    """

    help = "Actualiza la tasa de cambio desde la web del BCV"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando actualización de tasa de cambio desde el BCV...")

        try:
            # 1. Descargar la página
            response = requests.get(URL_BCV, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Lanza un error si la petición falla

            # 2. Analizar el HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # 3. Encontrar el elemento
            # Este es el 'selector' clave. Buscamos el div con id="dolar"
            # y dentro, la etiqueta <strong>
            tasa_div = soup.find("div", id="dolar")
            if tasa_div is None:
                raise Exception("No se encontró el <div> con id='dolar' en la página.")

            tasa_string = tasa_div.find("strong").text.strip()

            # 4. Limpiar el valor
            # El BCV usa formato "40,50" (coma decimal)
            tasa_limpia = tasa_string.replace(".", "").replace(",", ".")
            valor_decimal = Decimal(tasa_limpia)

            # 5. Guardar en la Base de Datos
            fecha_hoy = datetime.date.today()

            # Usamos get_or_create para evitar duplicados.
            # Si ya existe una tasa para 'fecha_hoy', no hará nada.
            # Si no existe, la creará.
            tasa_obj, created = TasaCambio.objects.get_or_create(
                fecha_vigencia=fecha_hoy, defaults={"valor": valor_decimal}
            )

            if created:
                # Si 'created' es True, significa que se guardó una nueva tasa
                self.stdout.write(
                    self.style.SUCCESS(
                        f"¡Éxito! Tasa nueva guardada para {fecha_hoy}: {valor_decimal} VES"
                    )
                )
            else:
                # Si 'created' es False, ya existía
                self.stdout.write(
                    self.style.WARNING(
                        f"La tasa para {fecha_hoy} ya estaba registrada ({tasa_obj.valor} VES)."
                    )
                )

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error al conectar con el BCV: {e}"))
        except Exception as e:
            # Captura cualquier otro error (ej: el HTML cambió y no encontramos el 'div')
            self.stderr.write(self.style.ERROR(f"Error inesperado: {e}"))
