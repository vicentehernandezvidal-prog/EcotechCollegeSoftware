# Python versión 3.14.6

# Se importan las librerías y módulos necesarios para el funcionamiento del programa.
# getpass permite ocultar la contraseña en la consola mientras se escribe.
from getpass import getpass

# Repositorios que se encargan de acceder a la base de datos para cada entidad.
from repositorios.usuario_repository import UsuarioRepository
from repositorios.empleado_repository import EmpleadoRepository
from repositorios.departamento_repository import DepartamentoRepository

# Servicio de autenticación para validar usuarios y crear cuentas.
from servicios.auth_service import AuthService

# Se importan los módulos de menús del sistema, cada uno representa una pantalla funcional.
# Estos menús se encuentran dentro de la carpeta "menus" del proyecto.
from menus.gestionar_departamentos import gestionar_departamentos
from menus.gestionar_proyectos import gestionar_proyectos
from menus.gestionar_registro_tiempo import gestionar_registro_tiempos
from menus.gestionar_informes import gestionar_informes
from menus.gestionar_apis import gestionar_apis
from menus.gestionar_administradores import gestionar_administradores
from menus.gestionar_datos_sensibles import gestionar_datos_sensibles

# Función que crea el primer administrador cuando no hay ningún usuario registrado en el sistema.
# Se ejecuta al inicio si la base de datos todavía no tiene cuentas de administrador.
def crear_administrador_inicial(auth):
    # Mensaje de bienvenida para la configuración inicial del sistema.
    print("\nNo existen cuentas. Configura el primer administrador.")

    # Se solicita la información básica del administrador inicial.
    nombre = input("Nombre de usuario: ").strip()
    correo = input("Correo: ").strip()
    password = getpass("Contraseña (mínimo 8 caracteres): ")
    confirmar = getpass("Repite la contraseña: ")

    # Validación simple para confirmar que ambas contraseñas coinciden.
    if password != confirmar:
        print("Las contraseñas no coinciden.")
        return False

    try:
        # Se crea el administrador usando el servicio de autenticación.
        creado = auth.crear_admin_inicial(nombre, password, correo)
        print("Administrador creado." if creado else "No se pudo crear el administrador.")
        return creado
    except ValueError as error:
        # Si la validación falla, se imprime el mensaje del servicio.
        print(error)
        return False


# Función para iniciar sesión del usuario dentro del sistema.
def iniciar_sesion(auth):
    print("\n--- INICIO DE SESIÓN ---")

    # Se piden el usuario y la contraseña desde la consola.
    nombre = input("Usuario: ").strip()
    password = getpass("Contraseña: ")

    # Se valida la información con AuthService.
    usuario = auth.autenticar(nombre, password)

    # Si no devuelve datos, las credenciales no son válidas.
    if not usuario:
        print("Credenciales incorrectas.")
    return usuario


# Función para registrar un empleado nuevo desde el menú principal.
def registrar_empleado(auth):
    # Se obtienen los departamentos existentes para asignarlos al empleado.
    deptos = DepartamentoRepository().listar()
    if not deptos:
        print("Primero debes crear un departamento.")
        return

    print("Departamentos disponibles:")
    for d in deptos:
        print(f"{d[0]} | {d[1]}")

    try:
        id_depto = int(input("ID departamento: "))
    except ValueError:
        print("ID no válido.")
        return

    # Se verifica que el ID ingresado exista en la lista.
    if id_depto not in [d[0] for d in deptos]:
        print("Departamento inexistente.")
        return

    # Se capturan los datos personales del empleado.
    nombre_usuario = input("Nombre de usuario: ").strip()
    correo = input("Correo: ").strip()
    rut = input("RUT: ").strip()
    primer_nombre = input("Primer nombre: ").strip()
    primer_apellido = input("Primer apellido: ").strip()
    password = getpass("Contraseña (mínimo 8 caracteres): ")

    try:
        # Se delega la creación del empleado al servicio de autenticación.
        ok = auth.registrar_empleado(nombre_usuario, password, correo, rut, id_depto, primer_nombre, primer_apellido)
        print("Empleado registrado." if ok else "No se pudo registrar el empleado.")
    except ValueError as error:
        print(error)


# Menú principal del sistema una vez que el usuario ya ha iniciado sesión.
def menu_principal(usuario):
    repo_usuarios = UsuarioRepository()

    while True:
        # Se imprime el encabezado del sistema con la sesión activa.
        print("\n" + "=" * 42)
        print("       ECOTECH SOLUTIONS")
        print(f" Sesión: {usuario['nombre']} ({usuario['rol']})")
        print("=" * 42)

        # Opciones disponibles del menú principal.
        print("1. Listar usuarios")
        print("2. Registrar empleado")
        print("3. Gestionar departamentos")
        print("4. Gestionar proyectos")
        print("5. Registro de tiempos")
        print("6. Informes")
        print("7. Servicios externos (clima/divisas)")
        print("8. Actualizar empleado")
        print("9. Eliminar empleado")
        print("10. Gestionar administradores")
        print("11. Datos sensibles de empleados")
        print("12. Cerrar sesión")

        op = input("> ").strip()

        # Opción 1: listar usuarios.
        if op == "1":
            if usuario["rol"] != "ADMINISTRADOR":
                print("Solo un administrador puede listar todas las cuentas.")
                continue
            for u in repo_usuarios.listar():
                print(f"{u[0]} | {u[1]} | {u[2]} | {u[3]}")

        # Opción 2: registrar empleado.
        elif op == "2":
            if usuario["rol"] == "ADMINISTRADOR":
                registrar_empleado(AuthService())
            else:
                print("Solo un administrador puede registrar empleados.")

        # Opción 3: menú de departamentos.
        elif op == "3":
            gestionar_departamentos()

        # Opción 4: menú de proyectos.
        elif op == "4":
            gestionar_proyectos()

        # Opción 5: registro de tiempos.
        elif op == "5":
            gestionar_registro_tiempos()

        # Opción 6: informes del sistema.
        elif op == "6":
            if usuario["rol"] == "ADMINISTRADOR":
                gestionar_informes(usuario)
            else:
                print("Solo un administrador puede gestionar informes.")

        # Opción 7: servicios externos (clima, divisas, etc.).
        elif op == "7":
            gestionar_apis()

        # Opción 8: actualizar empleado.
        elif op == "8":
            if usuario["rol"] != "ADMINISTRADOR":
                print("Solo un administrador puede modificar empleados.")
                continue
            repo = EmpleadoRepository()
            for e in repo.listar():
                print(f"{e[0]} | {e[2]} | RUT: {e[1]} | {e[3]}")
            try:
                id_emp = int(input("ID empleado: "))
                ok = repo.actualizar(
                    id_emp,
                    input("Nuevo RUT: ").strip(),
                    input("Nuevo usuario: ").strip(),
                    input("Nuevo correo: ").strip()
                )
                print("Empleado actualizado." if ok else "No se pudo actualizar.")
            except ValueError:
                print("ID no válido.")

        # Opción 9: eliminar empleado.
        elif op == "9":
            if usuario["rol"] != "ADMINISTRADOR":
                print("Solo un administrador puede eliminar empleados.")
                continue
            repo = EmpleadoRepository()
            for e in repo.listar():
                print(f"{e[0]} | {e[2]} | RUT: {e[1]}")
            try:
                id_emp = int(input("ID empleado: "))
                if input("¿Confirmas la eliminación? (S/N): ").strip().upper() == "S":
                    print("Empleado eliminado." if repo.eliminar(id_emp) else "No se pudo eliminar.")
            except ValueError:
                print("ID no válido.")

        # Opción 10: administración de usuarios administradores.
        elif op == "10":
            if usuario["rol"] == "ADMINISTRADOR":
                gestionar_administradores(usuario["id_usuario"])
            else:
                print("Solo un administrador puede gestionar administradores.")

        # Opción 11: acceso a datos sensibles de empleados.
        elif op == "11":
            if usuario["rol"] == "ADMINISTRADOR":
                gestionar_datos_sensibles()
            else:
                print("Solo un administrador puede gestionar datos sensibles.")

        # Opción 12: cerrar sesión y volver al inicio.
        elif op == "12":
            return

        # Si se ingresa una opción no válida, se informa al usuario.
        else:
            print("Opción no válida.")


# Función principal del programa.
# Se encarga de verificar si hay usuarios registrados y, si no, crear el primer administrador.
def main():
    auth = AuthService()

    while True:
        # Se consulta la lista de usuarios en la base de datos.
        usuarios = UsuarioRepository().listar()

        # Si no existen usuarios, se fuerza la creación del administrador inicial.
        if not usuarios:
            if not crear_administrador_inicial(auth):
                continue

        # Luego de asegurar que existe al menos un usuario, se inicia sesión.
        usuario = iniciar_sesion(auth)
        if usuario:
            menu_principal(usuario)


if __name__ == "__main__":
    main()
