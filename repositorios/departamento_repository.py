from repositorios.base_repository import BaseRepository

class DepartamentoRepository(BaseRepository):
    def guardar(self, nombre): return self._ejecutar("INSERT INTO DEPARTAMENTO (nombre_dept) VALUES (%s)", (nombre,))
    def listar(self): return self._ejecutar("SELECT id_departamento,nombre_dept,id_gerente FROM DEPARTAMENTO ORDER BY id_departamento", fetch=True)
    def actualizar(self, id_departamento, nombre): return self._ejecutar("UPDATE DEPARTAMENTO SET nombre_dept=%s WHERE id_departamento=%s", (nombre,id_departamento))
    def eliminar(self, id_departamento): return self._ejecutar("DELETE FROM DEPARTAMENTO WHERE id_departamento=%s", (id_departamento,))
