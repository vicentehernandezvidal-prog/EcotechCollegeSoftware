from repositorios.departamento_repository import DepartamentoRepository

def gestionar_departamentos():
    repo = DepartamentoRepository()
    while True:
        print("\n--- DEPARTAMENTOS ---\n1. Crear\n2. Listar\n3. Actualizar\n4. Eliminar\n5. Volver")
        op = input("> ").strip()
        try:
            if op == "1":
                nombre = input("Nombre: ").strip()
                if nombre: repo.guardar(nombre); print("Operación procesada.")
            elif op == "2":
                for d in repo.listar(): print(f"ID {d[0]} | {d[1]} | Gerente: {d[2]}")
            elif op == "3": repo.actualizar(int(input("ID: ")), input("Nuevo nombre: ").strip()); print("Operación procesada.")
            elif op == "4": repo.eliminar(int(input("ID: "))); print("Operación procesada.")
            elif op == "5": return
            else: print("Opción no válida.")
        except ValueError: print("Ingresa un número válido.")
