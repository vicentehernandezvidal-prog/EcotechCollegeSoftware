from repositorios.informe_repository import InformeRepository
from repositorios.administrador_repository import AdministradorRepository

def gestionar_informes(usuario):
    repo = InformeRepository(); admins = AdministradorRepository()
    while True:
        print("\n--- INFORMES ---\n1. Registrar informe\n2. Listar\n3. Eliminar\n4. Volver")
        op = input("> ").strip()
        try:
            if op == "1":
                admin = next((a for a in admins.listar() if a[1] == usuario["id_usuario"]), None)
                if not admin: print("El usuario autenticado no tiene perfil de administrador."); continue
                tipo = input("Tipo de contenido: ").strip()
                formato = input("Formato (PDF/EXCEL): ").strip().upper()
                if formato not in ("PDF","EXCEL"): print("Formato no válido."); continue
                repo.guardar(tipo,formato,admin[0]); print("Operación procesada.")
            elif op == "2":
                for i in repo.listar(): print(f"{i[0]} | {i[1]} | {i[2]} | Admin {i[3]} | {i[4]}")
            elif op == "3": repo.eliminar(int(input("ID informe: "))); print("Operación procesada.")
            elif op == "4": return
            else: print("Opción no válida.")
        except ValueError: print("Ingresa un ID válido.")
