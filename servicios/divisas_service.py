from decimal import Decimal, InvalidOperation
import requests

class DivisasService:
    URL = "https://cl.dolarapi.com/v1/cotizaciones"

    def consultar(self):
        try:
            respuesta = requests.get(self.URL, timeout=10)
            respuesta.raise_for_status()
            datos = respuesta.json()
            if not isinstance(datos, list):
                raise RuntimeError("El servicio de divisas entregó un formato inesperado.")
            return datos
        except requests.Timeout:
            raise RuntimeError("La consulta de divisas excedió el tiempo de espera.")
        except requests.ConnectionError:
            raise RuntimeError("No fue posible conectar con el servicio de divisas.")
        except requests.HTTPError:
            raise RuntimeError("El servicio de divisas respondió con un error HTTP.")
        except (requests.RequestException, ValueError):
            raise RuntimeError("No fue posible procesar la información de divisas.")

    def calcular_pago_desde_clp(self, monto_clp, moneda, cotizaciones):
        """Convierte CLP a moneda extranjera usando la cotización de venta (CLP por unidad)."""
        try:
            monto = Decimal(str(monto_clp))
        except InvalidOperation:
            raise ValueError("El monto debe ser numérico.")
        if not monto.is_finite() or monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        moneda = moneda.strip().upper()
        if not moneda or len(moneda) != 3 or not moneda.isalpha():
            raise ValueError("Código de moneda no válido.")
        cotizacion = next((c for c in cotizaciones if str(c.get("moneda", "")).upper() == moneda), None)
        if cotizacion is None:
            raise ValueError("No se encontró una cotización para esa moneda.")
        try:
            valor_venta = Decimal(str(cotizacion["venta"]))
        except (KeyError, InvalidOperation):
            raise RuntimeError("La cotización no contiene un valor de venta válido.")
        if not valor_venta.is_finite() or valor_venta <= 0:
            raise RuntimeError("El servicio entregó un valor de venta inválido.")
        return monto / valor_venta, valor_venta


# PARA MOSTRAR LAS DIVISAS DENTRO DEL MENU DE DATOS SENCIBLES, IMPLEMENTACION  API

    def monedas_disponibles(self, cotizaciones):
        return sorted({str(c.get("moneda", "")).upper() for c in cotizaciones if c.get("moneda")})
        