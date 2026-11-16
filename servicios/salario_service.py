from decimal import Decimal, InvalidOperation


class SalarioService:
    """Orquesta: repositorio (BD) + cifrado + divisas. No imprime nada."""

    def __init__(self, repo, cifrado, divisas):
        self._repo = repo
        self._cifrado = cifrado
        self._divisas = divisas




    def consultar_salario(self, id_empleado, moneda="CLP", cotizaciones=None):
        """Devuelve (monto, tasa) o None si no hay salario. tasa es None si la moneda es CLP."""
        token = self._repo.obtener_salario_cifrado(id_empleado)
        if token is None:
            return None
        try:
            salario_clp = Decimal(self._cifrado.descifrar(token))
        except InvalidOperation:
            raise RuntimeError("El salario almacenado no tiene un formato válido.")

        moneda = moneda.strip().upper()
        if moneda == "CLP":
            return salario_clp, None
        if not cotizaciones:
            raise RuntimeError("No hay cotizaciones disponibles para convertir.")
        return self._divisas.calcular_pago_desde_clp(salario_clp, moneda, cotizaciones)