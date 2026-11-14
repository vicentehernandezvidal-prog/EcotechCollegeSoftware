from getpass import getpass
from servicios.auth_service import AuthService
from repositorios.administrador_repository import AdministradorRepository


def gestionar_administradores(id_usuario_actual):
    auth = AuthService()
    repo = AdministradorRepository()
    while True:
        print("\n--- ADMINISTRADORES ---\n1. Registrar\n2. Listar\n3. Actualizar\n4. Eliminar\n5. Volver")
        op = input("> ").strip()
        try:
            if op == "1":
                nombre = input("Nombre de usuario: ").strip()
                correo = input("Correo: ").strip()
                password = getpass("Contraseña (mínimo 8 caracteres): ")
                confirmar = getpass("Repite la contraseña: ")
                if password != confirmar:
                    print("Las contraseñas no coinciden.")
                    continue
                ok = auth.registrar_admin(nombre,password,correo)
                print("Administrador registrado." if ok else "No se pudo registrar.")
            elif op == "2":
                for a in repo.listar(): print(f"ID Admin: {a[0]} | Usuario ID: {a[1]} | {a[2]} | {a[3]}")
            elif op == "3":
                for a in repo.listar(): print(f"ID Admin: {a[0]} | {a[2]} | {a[3]}")
                id_admin = int(input("ID administrador: "))
                nombre = input("Nuevo nombre de usuario: ").strip()
                correo = input("Nuevo correo: ").strip()
                print("Administrador actualizado." if repo.actualizar(id_admin,nombre,correo) else "No se pudo actualizar.")
            elif op == "4":
                for a in repo.listar(): print(f"ID Admin: {a[0]} | {a[2]}")
                id_admin = int(input("ID administrador: "))
                if any(a[0] == id_admin and a[1] == id_usuario_actual for a in repo.listar()):
                    print("No puedes eliminar la cuenta con la que iniciaste sesión.")
                    continue
                if input("¿Confirmas la eliminación? (S/N): ").strip().upper() == "S":
                    print("Administrador eliminado." if repo.eliminar(id_admin) else "No se pudo eliminar.")
            elif op == "5": return
            else: print("Opción no válida.")
        except ValueError: print("Ingresa un ID válido.")
