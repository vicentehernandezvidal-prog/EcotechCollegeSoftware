from decimal import Decimal, InvalidOperation
import requests

# api (aplication programming interface) siempre se me olvidan las siglas xdd

class DivisasService:
    # URL pública del servicio externo que entrega las cotizaciones de monedas.
    URL = "https://cl.dolarapi.com/v1/cotizaciones"

    def consultar(self):
        try:
            # Se hace la petición HTTP para obtener las cotizaciones actuales.
            respuesta = requests.get(self.URL, timeout=10)
            # Si la respuesta no es exitosa, se lanza una excepción para manejar el error.
            respuesta.raise_for_status()

            # Se convierte la respuesta JSON a un objeto Python.
            datos = respuesta.json()

            # El servicio debe devolver una lista de cotizaciones.
            if not isinstance(datos, list):
                raise RuntimeError("El servicio de divisas entregó un formato inesperado.")
            return datos

        # Si la petición tarda demasiado, se informa que hubo timeout.
        except requests.Timeout:
            raise RuntimeError("La consulta de divisas excedió el tiempo de espera.")
        # Si no hay conexión con el servidor, se indica el problema de red.
        except requests.ConnectionError:
            raise RuntimeError("No fue posible conectar con el servicio de divisas.")
        # Si el servidor responde con un código HTTP de error.
        except requests.HTTPError:
            raise RuntimeError("El servicio de divisas respondió con un error HTTP.")
        # Si la respuesta no se puede interpretar o el JSON está mal formado.
        except (requests.RequestException, ValueError):
            raise RuntimeError("No fue posible procesar la información de divisas.")

    def calcular_pago_desde_clp(self, monto_clp, moneda, cotizaciones):
        """Convierte CLP a moneda extranjera usando la cotización de venta (CLP por unidad)."""
        try:
            # Se convierte el monto a Decimal para trabajar con precisión financiera.
            monto = Decimal(str(monto_clp))
        except InvalidOperation:
            raise ValueError("El monto debe ser numérico.")

        # El monto debe ser finito y positivo para evitar cálculos inválidos.
        if not monto.is_finite() or monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        # Se normaliza el código de la moneda para compararlo sin importar mayúsculas/minúsculas.
        moneda = moneda.strip().upper()
        if not moneda or len(moneda) != 3 or not moneda.isalpha():
            raise ValueError("Código de moneda no válido.")

        # Se busca la cotización específica de la moneda solicitada dentro de la lista recibida.
        cotizacion = next((c for c in cotizaciones if str(c.get("moneda", "")).upper() == moneda), None)
        if cotizacion is None:
            raise ValueError("No se encontró una cotización para esa moneda.")

        try:
            # Se extrae el valor de venta que representa cuántos CLP vale una unidad de la moneda.
            valor_venta = Decimal(str(cotizacion["venta"]))
        except (KeyError, InvalidOperation):
            raise RuntimeError("La cotización no contiene un valor de venta válido.")

        # Se valida que la cotización entregue un valor útil y positivo.
        if not valor_venta.is_finite() or valor_venta <= 0:
            raise RuntimeError("El servicio entregó un valor de venta inválido.")

        # La conversión se hace dividiendo el monto en CLP por la cotización de venta.
        return monto / valor_venta, valor_venta

    # Este bloque se usa para mostrar las monedas disponibles en el menú de datos sensibles.
    # Funciona como una utilidad para listar códigos válidos que vienen desde la API.
    def monedas_disponibles(self, cotizaciones):
        # Se recorre la lista de cotizaciones, se extrae el código de cada moneda y se elimina duplicados.
        return sorted({str(c.get("moneda", "")).upper() for c in cotizaciones if c.get("moneda")})
        