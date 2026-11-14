from servicios.clima_service import ClimaService
from servicios.divisas_service import DivisasService

def gestionar_apis():
    while True:
        print("\n--- SERVICIOS EXTERNOS ---\n1. Consultar clima\n2. Consultar tipos de cambio\n3. Volver")
        op = input("> ").strip()
        try:
            if op == "1":
                ciudad = input("Ciudad: ")
                datos = ClimaService().consultar(ciudad)
                if datos is None: print("No se encontró esa ciudad.")
                else: print(f"{datos['ciudad']}, {datos['pais']} | Temperatura: {datos['temperatura']} °C | Humedad: {datos['humedad']}% | Estado: {datos['estado']}")
            elif op == "2":
                datos = DivisasService().consultar()
                if not datos: print("No hay cotizaciones disponibles.")
                for item in datos:
                    print(f"{item.get('moneda','N/D')} - {item.get('nombre','Divisa')} | Compra: {item.get('compra','N/D')} CLP | Venta: {item.get('venta','N/D')} CLP | Actualización: {item.get('fechaActualizacion','N/D')}")
                moneda = input("Código de moneda para calcular el pago (ej. USD, EUR): ").strip().upper()
                monto = input("Monto del pago en pesos chilenos (CLP): ").strip()
                convertido, valor_venta = DivisasService().calcular_pago_desde_clp(monto, moneda, datos)
                print(f"\nPago estimado: {convertido:.2f} {moneda}")
                print(f"Tipo de cambio aplicado: 1 {moneda} = {valor_venta} CLP (cotización de venta)")
            elif op == "3": return
            else: print("Opción no válida.")
        except (ValueError, RuntimeError) as error: print(f"[AVISO] {error}")
