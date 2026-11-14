# python version 3.14.6
# DOCUMENTO MAIN 

from getpass import getpass
from repositorios.usuario_repository import UsuarioRepository
from repositorios.empleado_repository import EmpleadoRepository
from repositorios.departamento_repository import DepartamentoRepository
from servicios.auth_service import AuthService
from menus.gestionar_departamentos import gestionar_departamentos
from menus.gestionar_proyectos import gestionar_proyectos
from menus.gestionar_registro_tiempo import gestionar_registro_tiempos
from menus.gestionar_informes import gestionar_informes
from menus.gestionar_apis import gestionar_apis
from menus.gestionar_administradores import gestionar_administradores


def crear_administrador_inicial(auth):
    print("\nNo existen cuentas. Configura el primer administrador.")
    nombre = input("Nombre de usuario: ").strip()
    correo = input("Correo: ").strip()
    password = getpass("Contraseña (mínimo 8 caracteres): ")
    confirmar = getpass("Repite la contraseña: ")
    if password != confirmar:
        print("Las contraseñas no coinciden."); return False
    try:
        creado = auth.crear_admin_inicial(nombre,password,correo)
        print("Administrador creado." if creado else "No se pudo crear el administrador.")
        return creado
    except ValueError as error:
        print(error); return False


def iniciar_sesion(auth):
    print("\n--- INICIO DE SESIÓN ---")
    nombre = input("Usuario: ").strip()
    password = getpass("Contraseña: ")
    usuario = auth.autenticar(nombre,password)
    if not usuario: print("Credenciales incorrectas.")
    return usuario


def registrar_empleado(auth):
    deptos = DepartamentoRepository().listar()
    if not deptos: print("Primero debes crear un departamento."); return
    print("Departamentos disponibles:")
    for d in deptos: print(f"{d[0]} | {d[1]}")
    try: id_depto = int(input("ID departamento: "))
    except ValueError: print("ID no válido."); return
    if id_depto not in [d[0] for d in deptos]: print("Departamento inexistente."); return
    nombre_usuario = input("Nombre de usuario: ").strip()
    correo = input("Correo: ").strip()
    rut = input("RUT: ").strip()
    primer_nombre = input("Primer nombre: ").strip()
    primer_apellido = input("Primer apellido: ").strip()
    password = getpass("Contraseña (mínimo 8 caracteres): ")
    try:
        ok = auth.registrar_empleado(nombre_usuario,password,correo,rut,id_depto,primer_nombre,primer_apellido)
        print("Empleado registrado." if ok else "No se pudo registrar el empleado.")
    except ValueError as error: print(error)


def menu_principal(usuario):
    repo_usuarios = UsuarioRepository()
    while True:
        print("\n" + "="*42)
        print("       ECOTECH SOLUTIONS")
        print(f" Sesión: {usuario['nombre']} ({usuario['rol']})")
        print("="*42)
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
        print("11. Cerrar sesión")
        op = input("> ").strip()
        if op == "1":
            if usuario["rol"] != "ADMINISTRADOR":
                print("Solo un administrador puede listar todas las cuentas.")
                continue
            for u in repo_usuarios.listar(): print(f"{u[0]} | {u[1]} | {u[2]} | {u[3]}")
        elif op == "2":
            if usuario["rol"] == "ADMINISTRADOR": registrar_empleado(AuthService())
            else: print("Solo un administrador puede registrar empleados.")
        elif op == "3": gestionar_departamentos()
        elif op == "4": gestionar_proyectos()
        elif op == "5": gestionar_registro_tiempos()
        elif op == "6":
            if usuario["rol"] == "ADMINISTRADOR": gestionar_informes(usuario)
            else: print("Solo un administrador puede gestionar informes.")
        elif op == "7": gestionar_apis()
        elif op == "8":
            if usuario["rol"] != "ADMINISTRADOR":
                print("Solo un administrador puede modificar empleados.")
                continue
            repo = EmpleadoRepository()
            for e in repo.listar(): print(f"{e[0]} | {e[2]} | RUT: {e[1]} | {e[3]}")
            try:
                id_emp = int(input("ID empleado: "))
                ok = repo.actualizar(id_emp, input("Nuevo RUT: ").strip(), input("Nuevo usuario: ").strip(), input("Nuevo correo: ").strip())
                print("Empleado actualizado." if ok else "No se pudo actualizar.")
            except ValueError: print("ID no válido.")
        elif op == "9":
            if usuario["rol"] != "ADMINISTRADOR":
                print("Solo un administrador puede eliminar empleados.")
                continue
            repo = EmpleadoRepository()
            for e in repo.listar(): print(f"{e[0]} | {e[2]} | RUT: {e[1]}")
            try:
                id_emp = int(input("ID empleado: "))
                if input("¿Confirmas la eliminación? (S/N): ").strip().upper() == "S":
                    print("Empleado eliminado." if repo.eliminar(id_emp) else "No se pudo eliminar.")
            except ValueError: print("ID no válido.")
        elif op == "10":
            if usuario["rol"] == "ADMINISTRADOR": gestionar_administradores(usuario["id_usuario"])
            else: print("Solo un administrador puede gestionar administradores.")
        elif op == "11": return
        else: print("Opción no válida.")


def main():
    auth = AuthService()
    while True:
        usuarios = UsuarioRepository().listar()
        if not usuarios:
            if not crear_administrador_inicial(auth): continue
        usuario = iniciar_sesion(auth)
        if usuario:
            menu_principal(usuario)


if __name__ == "__main__":
    main()
