import re
from decimal import Decimal, InvalidOperation
from repositorios.empleado_repository import EmpleadoRepository
from seguridad.cifrado_service import CifradoService


def _pedir_datos():
    direccion = input("Dirección: ").strip()
    if not 5 <= len(direccion) <= 200:
        raise ValueError("La dirección debe tener entre 5 y 200 caracteres.")
    telefono = input("Teléfono: ").strip()
    if not re.fullmatch(r"\+?[0-9 ()-]{7,20}", telefono):
        raise ValueError("Teléfono no válido (7 a 20 dígitos, puede incluir +, espacios, guiones o paréntesis).")
    try:
        salario = Decimal(input("Salario (CLP): ").strip())
    except InvalidOperation:
        raise ValueError("El salario debe ser numérico.")
    if not salario.is_finite() or not 0 < salario <= Decimal("100000000"):
        raise ValueError("El salario debe ser mayor que cero y razonable.")
    return direccion, telefono, str(salario)


def gestionar_datos_sensibles():
    repo = EmpleadoRepository()
    try:
        cifrado = CifradoService()
    except RuntimeError as error:
        print(f"[AVISO] {error}")
        return
    while True:
        print("\n--- DATOS SENSIBLES DE EMPLEADOS ---\n1. Registrar/actualizar\n2. Consultar\n3. Volver")
        op = input("> ").strip()
        try:
            if op in ("1", "2"):
                for e in repo.listar():
                    print(f"{e[0]} | {e[5]} {e[6]} | RUT: {e[1]}")
                id_emp = int(input("ID empleado: "))
                if id_emp not in repo.ids_validos():
                    print("Empleado inexistente.")
                    continue
                if op == "1":
                    d, t, s = _pedir_datos()
                    ok = repo.guardar_datos_sensibles(id_emp, cifrado.cifrar(d), cifrado.cifrar(t), cifrado.cifrar(s))
                    print("Datos guardados cifrados." if ok else "No se pudo guardar.")
                else:
                    fila = repo.obtener_datos_sensibles(id_emp)
                    if not fila or all(c is None for c in fila):
                        print("Este empleado no tiene datos sensibles registrados.")
                        continue
                    d, t, s = (cifrado.descifrar(c) for c in fila)
                    print(f"Dirección: {d}\nTeléfono: {t}\nSalario: {s} CLP")
            elif op == "3":
                return
            else:
                print("Opción no válida.")
        except ValueError as error:
            print(f"[AVISO] {error}")
        except RuntimeError as error:
            print(f"[AVISO] {error}")