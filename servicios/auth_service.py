import pymysql
import re  # Librería para validar cadenas con expresiones regulares.
from database.conexion import Conexion  # Clase encargada de abrir la conexión a la base de datos.
from seguridad.password_service import PasswordService  # Servicio que genera y verifica contraseñas cifradas.


class AuthService:
    def __init__(self):  # Se ejecuta al crear una instancia de la clase.
        # Se guarda un objeto con la lógica de hashing y comparación de contraseñas.
        self.passwords = PasswordService()

    def _crear_cuenta(self, nombre, password, correo, rol, datos_perfil=None):
        """Crea usuario y perfil en una sola transacción para evitar cuentas incompletas."""
        # Se limpia el nombre y el correo antes de validar para evitar problemas con espacios extras.
        nombre = nombre.strip()
        correo = correo.strip()

        # Se valida que el nombre tenga el formato permitido: letras, números y algunos caracteres especiales.
        # Si no cumple la regla, se rechaza la cuenta antes de consultar la base de datos.
        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,50}", nombre):
            raise ValueError("El usuario debe tener entre 3 y 50 caracteres: letras, números, punto, guion o guion bajo.")

        # Se valida el formato del correo con una expresión regular común y también se limita su longitud.
        # Esto ayuda a prevenir entradas inválidas o extremadamente largas.
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo) or len(correo) > 254:
            raise ValueError("Ingresa un correo electrónico válido.")

        # Se cifra la contraseña antes de guardarla en la base de datos.
        # Nunca se almacena la contraseña en texto plano.
        hash_password = self.passwords.generar_hash(password)

        # Se intenta abrir la conexión con la base de datos.
        conexion = Conexion.conectar()
        if conexion is None:
            return False

        try:
            with conexion.cursor() as cursor:
                # Se inserta el usuario principal en la tabla USUARIO.
                # Los %s son placeholders para evitar inyección SQL y mantener los valores seguros.
                cursor.execute(
                    "INSERT INTO USUARIO (nombre_usuario,hash_password,correo,rol) VALUES (%s,%s,%s,%s)",
                    (nombre, hash_password, correo, rol)
                )

                # lastrowid devuelve el identificador generado automáticamente para el usuario recién insertado.
                id_usuario = cursor.lastrowid

                # Si el rol es administrador, se crea un registro en la tabla ADMINISTRADOR usando el mismo id_user.
                if rol == "ADMINISTRADOR":
                    cursor.execute("INSERT INTO ADMINISTRADOR (id_usuario) VALUES (%s)", (id_usuario,))

                # Si es un empleado, se necesitan datos adicionales del perfil personal.
                # Se desempaca la tupla con RUT, departamento, nombre y apellido para crear el registro asociado.
                elif rol == "EMPLEADO":
                    rut, id_departamento, primer_nombre, primer_apellido = datos_perfil
                    cursor.execute(
                        "INSERT INTO EMPLEADO (rut,id_usuario,id_departamento,primer_nombre,primer_apellido,inicio_contrato) VALUES (%s,%s,%s,%s,%s,CURDATE())",
                        (rut, id_usuario, id_departamento, primer_nombre, primer_apellido)
                    )

            # Si todo salió bien, se confirma la transacción para guardar los cambios.
            conexion.commit()
            return True

        # IntegrityError indica que hubo una violación de restricciones, como duplicados o claves ajenas inválidas.
        except pymysql.IntegrityError:
            conexion.rollback()
            print("[ERROR] No se pudo crear la cuenta. Verifica que usuario, correo o RUT no estén repetidos y que los datos relacionados existan.")
            return False

        # MySQLError cubre otros errores generales de base de datos.
        except pymysql.MySQLError:
            conexion.rollback()
            print("[ERROR] No se pudo crear la cuenta en la base de datos.")
            return False

        finally:
            # Siempre se cierra la conexión para liberar recursos del sistema.
            conexion.close()

    def crear_admin_inicial(self, nombre, password, correo):
        # Crea el primer administrador sin pedir información adicional.
        return self._crear_cuenta(nombre, password, correo, "ADMINISTRADOR")

    def registrar_admin(self, nombre, password, correo):
        # Registro estándar de un administrador desde la aplicación.
        return self._crear_cuenta(nombre, password, correo, "ADMINISTRADOR")

    def autenticar(self, nombre, password):
        # Si el nombre o la contraseña vienen vacíos, se rechaza la autenticación imediatamente.
        if not nombre.strip() or not password:
            return None

        # Se establece la conexión para consultar el usuario en la base de datos.
        conexion = Conexion.conectar()
        if conexion is None:
            return None

        try:
            with conexion.cursor() as cursor:
                # Busca el usuario por nombre de usuario, que debe coincidir exactamente con el valor almacenado.
                cursor.execute("SELECT id_usuario,nombre_usuario,hash_password,correo,rol FROM USUARIO WHERE nombre_usuario=%s", (nombre.strip(),))
                fila = cursor.fetchone()

            # Si no existe la fila o la contraseña no coincide, la autenticación falla.
            if not fila or not self.passwords.verificar(password, fila[2]):
                return None

            # Si la credencial es válida, se devuelve un diccionario con los datos públicos del usuario.
            return {"id_usuario": fila[0], "nombre": fila[1], "correo": fila[3], "rol": fila[4]}

        except pymysql.MySQLError:
            # Error al consultar la BD durante la validación de credenciales.
            print("[ERROR] No fue posible validar las credenciales.")
            return None
        finally:
            # Se cierra la conexión al terminar la consulta.
            conexion.close()

    def registrar_empleado(self, nombre_usuario, password, correo, rut, id_departamento, primer_nombre, primer_apellido):
        # Se validan los datos obligatorios del empleado antes de crear la cuenta.
        if not rut.strip() or not primer_nombre.strip() or not primer_apellido.strip():
            raise ValueError("RUT, nombre y apellido son obligatorios.")

        # Se arma la tupla con la información adicional del perfil del empleado.
        datos = (rut.strip(), id_departamento, primer_nombre.strip(), primer_apellido.strip())

        # Se reutiliza la lógica común para crear la cuenta y el perfil del empleado.
        return self._crear_cuenta(nombre_usuario, password, correo, "EMPLEADO", datos)
