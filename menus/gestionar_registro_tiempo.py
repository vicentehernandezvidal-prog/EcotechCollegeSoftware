from repositorios.registro_tiempo_repository import RegistroTiempoRepository
from repositorios.empleado_repository import EmpleadoRepository
from repositorios.proyecto_repository import ProyectoRepository

def gestionar_registro_tiempos():
    repo = RegistroTiempoRepository(); empleados = EmpleadoRepository(); proyectos = ProyectoRepository()
    while True:
        print("\n--- REGISTRO DE TIEMPOS ---\n1. Registrar horas\n2. Listar\n3. Validar\n4. Eliminar\n5. Volver")
        op = input("> ").strip()
        try:
            if op == "1":
                print("Empleados:")
                for e in empleados.listar(): print(f"{e[0]} | {e[2]} | {e[1]}")
                id_emp = int(input("ID empleado: "))
                if id_emp not in empleados.ids_validos(): print("Empleado inexistente."); continue
                proys = proyectos.listar()
                for p in proys: print(f"{p[0]} | {p[1]}")
                id_proy = int(input("ID proyecto: "))
                if id_proy not in [p[0] for p in proys]: print("Proyecto inexistente."); continue
                horas = float(input("Horas (máximo 24): "))
                if not 0 < horas <= 24: print("Las horas deben estar entre 0 y 24."); continue
                desc = input("Descripción: ").strip()
                repo.guardar(id_emp,id_proy,horas,desc); print("Operación procesada.")
            elif op == "2":
                for r in repo.listar(): print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} h | {r[6]} | {r[5]}")
            elif op == "3":
                estado = input("Estado (APROBADO/RECHAZADO): ").strip().upper()
                if estado not in ("APROBADO","RECHAZADO"): print("Estado no válido."); continue
                repo.validar(int(input("ID registro: ")),estado); print("Operación procesada.")
            elif op == "4": repo.eliminar(int(input("ID registro: "))); print("Operación procesada.")
            elif op == "5": return
            else: print("Opción no válida.")
        except ValueError: print("Ingresa valores numéricos válidos.")
