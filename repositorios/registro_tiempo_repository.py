from repositorios.base_repository import BaseRepository

class RegistroTiempoRepository(BaseRepository):
    def guardar(self, id_empleado, id_proyecto, horas, descripcion):
        return self._ejecutar("INSERT INTO REGISTRO_TIEMPO (id_empleado,id_proyecto,fecha,horas,descripcion_tarea,estado_validacion) VALUES (%s,%s,CURDATE(),%s,%s,'PENDIENTE')", (id_empleado,id_proyecto,horas,descripcion))
    def listar(self):
        sql = "SELECT r.id_registro,u.nombre_usuario,p.nombre,r.fecha,r.horas,r.descripcion_tarea,r.estado_validacion FROM REGISTRO_TIEMPO r JOIN EMPLEADO e ON r.id_empleado=e.id_empleado JOIN USUARIO u ON e.id_usuario=u.id_usuario JOIN PROYECTO p ON r.id_proyecto=p.id_proyecto ORDER BY r.fecha DESC"
        return self._ejecutar(sql, fetch=True)
    def validar(self, id_registro, estado):
        if estado not in ("APROBADO", "RECHAZADO"): return False
        return self._ejecutar("UPDATE REGISTRO_TIEMPO SET estado_validacion=%s WHERE id_registro=%s", (estado,id_registro))
    def eliminar(self, id_registro): return self._ejecutar("DELETE FROM REGISTRO_TIEMPO WHERE id_registro=%s", (id_registro,))
