from repositorios.base_repository import BaseRepository
class EmpleadoRepository(BaseRepository):
    def crear_perfil(self, rut, id_usuario, id_departamento, primer_nombre, primer_apellido):
        sql = "INSERT INTO EMPLEADO (rut,id_usuario,id_departamento,primer_nombre,primer_apellido,inicio_contrato) VALUES (%s,%s,%s,%s,%s,CURDATE())"
        return self._ejecutar(sql, (rut,id_usuario,id_departamento,primer_nombre,primer_apellido))
    def listar(self):
        sql = "SELECT e.id_empleado,e.rut,u.nombre_usuario,u.correo,d.nombre_dept,e.primer_nombre,e.primer_apellido FROM EMPLEADO e JOIN USUARIO u ON e.id_usuario=u.id_usuario JOIN DEPARTAMENTO d ON e.id_departamento=d.id_departamento ORDER BY e.id_empleado"
        return self._ejecutar(sql, fetch=True)
    def ids_validos(self):
        return [fila[0] for fila in self._ejecutar("SELECT id_empleado FROM EMPLEADO", fetch=True)]
    def actualizar(self, id_empleado, rut, nombre_usuario, correo):
        from database.conexion import Conexion
        import pymysql
        conexion = Conexion.conectar()
        if conexion is None: return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM EMPLEADO WHERE id_empleado=%s", (id_empleado,))
                fila = cursor.fetchone()
                if not fila: return False
                cursor.execute("UPDATE EMPLEADO SET rut=%s WHERE id_empleado=%s", (rut,id_empleado))
                cursor.execute("UPDATE USUARIO SET nombre_usuario=%s,correo=%s WHERE id_usuario=%s", (nombre_usuario,correo,fila[0]))
            conexion.commit(); return True
        except pymysql.MySQLError:
            conexion.rollback(); print("[ERROR] No se pudo actualizar el empleado."); return False
        finally: conexion.close()
    def eliminar(self, id_empleado):
        from database.conexion import Conexion
        import pymysql
        conexion = Conexion.conectar()
        if conexion is None: return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM EMPLEADO WHERE id_empleado=%s", (id_empleado,))
                fila = cursor.fetchone()
                if not fila: return False
                cursor.execute("DELETE FROM EMPLEADO WHERE id_empleado=%s", (id_empleado,))
                cursor.execute("DELETE FROM USUARIO WHERE id_usuario=%s", (fila[0],))
            conexion.commit(); return True
        except pymysql.MySQLError:
            conexion.rollback(); print("[ERROR] No se pudo eliminar el empleado. Puede tener registros relacionados."); return False
        finally: conexion.close()



# ----------------PARA EL CIFRADO DE LOS DATOS SEGUN LA BD

    def guardar_datos_sensibles(self, id_empleado, direccion_cif, telefono_cif, salario_cif):
        sql = "UPDATE EMPLEADO SET direccion_cifrada=%s, telefono_cifrado=%s, salario_cifrado=%s WHERE id_empleado=%s"
        return self._ejecutar(sql, (direccion_cif, telefono_cif, salario_cif, id_empleado))



    def obtener_datos_sensibles(self, id_empleado):
        sql = "SELECT direccion_cifrada, telefono_cifrado, salario_cifrado FROM EMPLEADO WHERE id_empleado=%s"
        filas = self._ejecutar(sql, (id_empleado,), fetch=True)
        return filas[0] if filas else None
