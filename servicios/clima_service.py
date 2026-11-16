import requests


class ClimaService:
    # URL para buscar una ciudad por nombre y obtener sus coordenadas geográficas.
    URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
    # URL para consultar el clima actual en una ubicación determinada.
    URL_PRONOSTICO = "https://api.open-meteo.com/v1/forecast"

    def consultar(self, ciudad):
        # Se limpia la entrada para evitar espacios innecesarios del usuario.
        ciudad = ciudad.strip()

        # Se valida que el nombre de la ciudad tenga un formato razonable.
        # Solo permite letras, espacios, guiones, apóstrofos y caracteres con tildes.
        if not ciudad or len(ciudad) > 100 or not all(c.isalpha() or c in " -'áéíóúÁÉÍÓÚñÑ" for c in ciudad):
            raise ValueError("Ingresa un nombre de ciudad válido.")

        try:
            # Primero se busca la ciudad en la API geocoding para obtener latitud y longitud.
            geo = requests.get(
                self.URL_GEOCODING,
                params={"name": ciudad, "count": 1, "language": "es", "format": "json"},
                timeout=10
            )
            geo.raise_for_status()

            # Se extrae la primera coincidencia del resultado.
            resultados = geo.json().get("results", [])
            if not resultados:
                return None
            lugar = resultados[0]

            # Con la ubicación obtenida, se consulta el clima actual del lugar.
            clima = requests.get(
                self.URL_PRONOSTICO,
                params={
                    "latitude": lugar["latitude"],
                    "longitude": lugar["longitude"],
                    "current": "temperature_2m,relative_humidity_2m,weather_code",
                    "timezone": "auto"
                },
                timeout=10
            )
            clima.raise_for_status()

            # Se extrae la información del clima actual del JSON de respuesta.
            actual = clima.json().get("current", {})
            codigo = actual.get("weather_code")

            # Mapeo de códigos meteorológicos a descripciones legibles en español.
            descripciones = {
                0: "Despejado",
                1: "Mayormente despejado",
                2: "Parcialmente nublado",
                3: "Nublado",
                45: "Niebla",
                48: "Niebla con escarcha",
                51: "Llovizna ligera",
                53: "Llovizna moderada",
                55: "Llovizna intensa",
                61: "Lluvia ligera",
                63: "Lluvia moderada",
                65: "Lluvia intensa",
                71: "Nevada ligera",
                73: "Nevada moderada",
                75: "Nevada intensa",
                80: "Chubascos ligeros",
                81: "Chubascos moderados",
                82: "Chubascos intensos",
                95: "Tormenta"
            }

            # Se retorna un diccionario con la información útil para mostrar en la interfaz.
            return {
                "ciudad": lugar.get("name", ciudad),
                "pais": lugar.get("country", ""),
                "temperatura": actual.get("temperature_2m"),
                "humedad": actual.get("relative_humidity_2m"),
                "estado": descripciones.get(codigo, "Condición no clasificada"),
                "codigo_clima": codigo
            }

        # Si la llamada tarda demasiado, se informa que el servicio tardó demasiado.
        except requests.Timeout:
            raise RuntimeError("La consulta del clima excedió el tiempo de espera.")
        # Si no hay conexión con el servicio externo, se notifica el fallo.
        except requests.ConnectionError:
            raise RuntimeError("No fue posible conectar con el servicio climático.")
        # Si el servicio responde con un error HTTP, se informa al usuario.
        except requests.HTTPError:
            raise RuntimeError("El servicio climático respondió con un error HTTP.")
        # Si el contenido no es válido, se captura como un error de procesamiento.
        except (requests.RequestException, ValueError, KeyError):
            raise RuntimeError("No fue posible procesar la información climática.")

