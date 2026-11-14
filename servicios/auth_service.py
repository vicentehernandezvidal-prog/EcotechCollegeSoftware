import pymysql
import re
from database.conexion import Conexion
from seguridad.password_service import PasswordService

class AuthService:
    def __init__(self):
        self.passwords = PasswordService()

    def _crear_cuenta(self, nombre, password, correo, rol, datos_perfil=None):
        """Crea usuario y perfil en una sola transacción para evitar cuentas incompletas."""
        nombre = nombre.strip()
        correo = correo.strip()
        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,50}", nombre):
            raise ValueError("El usuario debe tener entre 3 y 50 caracteres: letras, números, punto, guion o guion bajo.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo) or len(correo) > 254:
            raise ValueError("Ingresa un correo electrónico válido.")
        hash_password = self.passwords.generar_hash(password)
        conexion = Conexion.conectar()
        if conexion is None:
            return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO USUARIO (nombre_usuario,hash_password,correo,rol) VALUES (%s,%s,%s,%s)",
                    (nombre, hash_password, correo, rol)
                )
                id_usuario = cursor.lastrowid
                if rol == "ADMINISTRADOR":
                    cursor.execute("INSERT INTO ADMINISTRADOR (id_usuario) VALUES (%s)", (id_usuario,))
                elif rol == "EMPLEADO":
                    rut, id_departamento, primer_nombre, primer_apellido = datos_perfil
                    cursor.execute(
                        "INSERT INTO EMPLEADO (rut,id_usuario,id_departamento,primer_nombre,primer_apellido,inicio_contrato) VALUES (%s,%s,%s,%s,%s,CURDATE())",
                        (rut,id_usuario,id_departamento,primer_nombre,primer_apellido)
                    )
            conexion.commit()
            return True
        except pymysql.IntegrityError:
            conexion.rollback()
            print("[ERROR] No se pudo crear la cuenta. Verifica que usuario, correo o RUT no estén repetidos y que los datos relacionados existan.")
            return False
        except pymysql.MySQLError:
            conexion.rollback()
            print("[ERROR] No se pudo crear la cuenta en la base de datos.")
            return False
        finally:
            conexion.close()

    def crear_admin_inicial(self, nombre, password, correo):
        return self._crear_cuenta(nombre, password, correo, "ADMINISTRADOR")

    def registrar_admin(self, nombre, password, correo):
        return self._crear_cuenta(nombre, password, correo, "ADMINISTRADOR")

    def autenticar(self, nombre, password):
        if not nombre.strip() or not password:
            return None
        conexion = Conexion.conectar()
        if conexion is None:
            return None
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_usuario,nombre_usuario,hash_password,correo,rol FROM USUARIO WHERE nombre_usuario=%s", (nombre.strip(),))
                fila = cursor.fetchone()
            if not fila or not self.passwords.verificar(password, fila[2]):
                return None
            return {"id_usuario": fila[0], "nombre": fila[1], "correo": fila[3], "rol": fila[4]}
        except pymysql.MySQLError:
            print("[ERROR] No fue posible validar las credenciales.")
            return None
        finally:
            conexion.close()

    def registrar_empleado(self, nombre_usuario, password, correo, rut, id_departamento, primer_nombre, primer_apellido):
        if not rut.strip() or not primer_nombre.strip() or not primer_apellido.strip():
            raise ValueError("RUT, nombre y apellido son obligatorios.")
        datos = (rut.strip(), id_departamento, primer_nombre.strip(), primer_apellido.strip())
        return self._crear_cuenta(nombre_usuario, password, correo, "EMPLEADO", datos)
