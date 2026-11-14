from repositorios.proyecto_repository import ProyectoRepository

def gestionar_proyectos():
    repo = ProyectoRepository()
    while True:
        print("\n--- PROYECTOS ---\n1. Crear\n2. Listar\n3. Actualizar\n4. Eliminar\n5. Volver")
        op = input("> ").strip()
        try:
            if op == "1": repo.guardar(input("Nombre: ").strip(), input("Descripción: ").strip()); print("Operación procesada.")
            elif op == "2":
                for p in repo.listar(): print(f"ID {p[0]} | {p[1]} | Inicio: {p[3]}\n{p[2]}")
            elif op == "3": repo.actualizar(int(input("ID: ")), input("Nuevo nombre: ").strip(), input("Nueva descripción: ").strip()); print("Operación procesada.")
            elif op == "4": repo.eliminar(int(input("ID: "))); print("Operación procesada.")
            elif op == "5": return
            else: print("Opción no válida.")
        except ValueError: print("Ingresa un número válido.")
