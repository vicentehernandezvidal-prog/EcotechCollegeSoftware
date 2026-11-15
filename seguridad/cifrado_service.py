import os
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()


class CifradoService:
    """Cifrado simétrico (Fernet) para datos sensibles. La clave se lee desde .env."""

    def __init__(self):
        clave = os.getenv("CLAVE_CIFRADO")
        if not clave:
            raise RuntimeError("Falta configurar CLAVE_CIFRADO en el archivo .env.")
        try:
            self._fernet = Fernet(clave.encode("ascii"))
        except (ValueError, TypeError):
            raise RuntimeError("La clave de cifrado configurada no es válida.")

    def cifrar(self, texto):
        if texto is None:
            return None
        return self._fernet.encrypt(str(texto).encode("utf-8"))

    def descifrar(self, token):
        if token is None:
            return None
        try:
            return self._fernet.decrypt(bytes(token)).decode("utf-8")
        except InvalidToken:
            # Mensaje genérico: no se expone la causa interna
            raise RuntimeError("No fue posible descifrar el dato (clave incorrecta o dato alterado).")