import requests

class ClimaService:
    URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
    URL_PRONOSTICO = "https://api.open-meteo.com/v1/forecast"

    def consultar(self, ciudad):
        ciudad = ciudad.strip()
        if not ciudad or len(ciudad) > 100 or not all(c.isalpha() or c in " -'áéíóúÁÉÍÓÚñÑ" for c in ciudad):
            raise ValueError("Ingresa un nombre de ciudad válido.")
        try:
            geo = requests.get(self.URL_GEOCODING, params={"name": ciudad, "count": 1, "language": "es", "format": "json"}, timeout=10)
            geo.raise_for_status()
            resultados = geo.json().get("results", [])
            if not resultados: return None
            lugar = resultados[0]
            clima = requests.get(self.URL_PRONOSTICO, params={
                "latitude": lugar["latitude"], "longitude": lugar["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code",
                "timezone": "auto"
            }, timeout=10)
            clima.raise_for_status()
            actual = clima.json().get("current", {})
            codigo = actual.get("weather_code")
            descripciones = {0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
                3: "Nublado", 45: "Niebla", 48: "Niebla con escarcha", 51: "Llovizna ligera",
                53: "Llovizna moderada", 55: "Llovizna intensa", 61: "Lluvia ligera",
                63: "Lluvia moderada", 65: "Lluvia intensa", 71: "Nevada ligera",
                73: "Nevada moderada", 75: "Nevada intensa", 80: "Chubascos ligeros",
                81: "Chubascos moderados", 82: "Chubascos intensos", 95: "Tormenta"}
            return {"ciudad": lugar.get("name", ciudad), "pais": lugar.get("country", ""),
                    "temperatura": actual.get("temperature_2m"),
                    "humedad": actual.get("relative_humidity_2m"),
                    "estado": descripciones.get(codigo, "Condición no clasificada"),
                    "codigo_clima": codigo}
        except requests.Timeout:
            raise RuntimeError("La consulta del clima excedió el tiempo de espera.")
        except requests.ConnectionError:
            raise RuntimeError("No fue posible conectar con el servicio climático.")
        except requests.HTTPError:
            raise RuntimeError("El servicio climático respondió con un error HTTP.")
        except (requests.RequestException, ValueError, KeyError):
            raise RuntimeError("No fue posible procesar la información climática.")
