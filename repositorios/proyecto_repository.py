from repositorios.base_repository import BaseRepository

class ProyectoRepository(BaseRepository):
    def guardar(self, nombre, descripcion): return self._ejecutar("INSERT INTO PROYECTO (nombre,descripcion,fecha_inicio) VALUES (%s,%s,CURDATE())", (nombre,descripcion))
    def listar(self): return self._ejecutar("SELECT id_proyecto,nombre,descripcion,fecha_inicio FROM PROYECTO ORDER BY id_proyecto", fetch=True)
    def actualizar(self, id_proyecto, nombre, descripcion): return self._ejecutar("UPDATE PROYECTO SET nombre=%s,descripcion=%s WHERE id_proyecto=%s", (nombre,descripcion,id_proyecto))
    def eliminar(self, id_proyecto): return self._ejecutar("DELETE FROM PROYECTO WHERE id_proyecto=%s", (id_proyecto,))
