import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import datetime

from django.core.management.base import BaseCommand
from tasa.models import TasaCambio

# URL oficial del BCV
URL_BCV = "https://www.bcv.org.ve/"

# Headers para simular ser un navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


class Command(BaseCommand):
    help = "Actualiza las tasas de cambio (USD y EUR) desde la web del BCV"

    def handle(self, *args, **options):
        self.stdout.write("Conectando al BCV...")

        try:
            # NOTA: Si tienes problemas de SSL localmente o en PA,
            # cambia verify=True a verify=False aquí abajo.
            response = requests.get(URL_BCV, headers=HEADERS, timeout=15, verify=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # --- 1. Extraer Dólar ---
            valor_usd = self.extraer_valor(soup, "dolar")
            if not valor_usd:
                self.stdout.write(self.style.ERROR("No se encontró el Dólar."))
                return

            # --- 2. Extraer Euro ---
            valor_eur = self.extraer_valor(soup, "euro")
            if not valor_eur:
                self.stdout.write(
                    self.style.WARNING("No se encontró el Euro (se guardará solo USD).")
                )

            # --- 3. Guardar/Actualizar en BD ---
            fecha_hoy = datetime.date.today()

            # Usamos update_or_create:
            # Busca por fecha_vigencia. Si existe, actualiza los 'defaults'.
            # Si no existe, crea uno nuevo.
            tasa_obj, created = TasaCambio.objects.update_or_create(
                fecha_vigencia=fecha_hoy,
                defaults={
                    "valor": valor_usd,  # Campo del USD
                    "valor_euro": valor_eur,  # Campo del EUR (nuevo)
                },
            )

            accion = "Creada" if created else "Actualizada"
            self.stdout.write(
                self.style.SUCCESS(
                    f"Tasa {accion} para {fecha_hoy} -> USD: {valor_usd} | EUR: {valor_eur}"
                )
            )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))

    def extraer_valor(self, soup, id_div):
        """
        Función auxiliar para buscar un div por ID, sacar el texto
        y convertirlo a Decimal.
        """
        div = soup.find("div", id=id_div)
        if not div:
            return None

        try:
            # Busca el strong dentro del div
            texto_sucio = div.find("strong").text.strip()
            # Reemplaza comas por puntos (formato 40,50 -> 40.50)
            texto_limpio = texto_sucio.replace(".", "").replace(",", ".")
            return Decimal(texto_limpio)
        except Exception:
            return None
