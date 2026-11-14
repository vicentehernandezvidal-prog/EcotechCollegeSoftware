import hashlib
import hmac
import secrets

class PasswordService:
    """Hash de contraseñas con PBKDF2. Las contraseñas no se cifran ni se guardan en texto plano."""
    ITERACIONES = 600_000
    ALGORITMO = "pbkdf2_sha256"

    def generar_hash(self, password):
        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, self.ITERACIONES)
        return f"{self.ALGORITMO}${self.ITERACIONES}${salt.hex()}${digest.hex()}".encode("ascii")

    def verificar(self, password, hash_guardado):
        try:
            if isinstance(hash_guardado, bytes): hash_guardado = hash_guardado.decode("ascii")
            algoritmo, iteraciones, salt_hex, digest_hex = hash_guardado.split("$")
            if algoritmo != self.ALGORITMO: return False
            calculado = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iteraciones))
            return hmac.compare_digest(calculado.hex(), digest_hex)
        except (ValueError, TypeError, AttributeError):
            return False
