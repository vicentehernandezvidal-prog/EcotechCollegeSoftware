from repositorios.base_repository import BaseRepository

class AdministradorRepository(BaseRepository):
    def crear_perfil(self, id_usuario):
        return self._ejecutar("INSERT INTO ADMINISTRADOR (id_usuario) VALUES (%s)", (id_usuario,))
    def listar(self):
        return self._ejecutar("SELECT a.id_admin,u.id_usuario,u.nombre_usuario,u.correo,u.rol FROM ADMINISTRADOR a JOIN USUARIO u ON a.id_usuario=u.id_usuario", fetch=True)
    def actualizar(self, id_admin, nombre_usuario, correo):
        from database.conexion import Conexion
        import pymysql
        conexion = Conexion.conectar()
        if conexion is None: return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM ADMINISTRADOR WHERE id_admin=%s", (id_admin,))
                fila = cursor.fetchone()
                if not fila: return False
                cursor.execute("UPDATE USUARIO SET nombre_usuario=%s,correo=%s WHERE id_usuario=%s", (nombre_usuario,correo,fila[0]))
            conexion.commit(); return True
        except pymysql.MySQLError:
            conexion.rollback(); print("[ERROR] No se pudo actualizar el administrador."); return False
        finally: conexion.close()

    def eliminar(self, id_admin):
        from database.conexion import Conexion
        import pymysql
        conexion = Conexion.conectar()
        if conexion is None: return False
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM ADMINISTRADOR WHERE id_admin=%s", (id_admin,))
                fila = cursor.fetchone()
                if not fila: return False
                cursor.execute("DELETE FROM ADMINISTRADOR WHERE id_admin=%s", (id_admin,))
                cursor.execute("DELETE FROM USUARIO WHERE id_usuario=%s", (fila[0],))
            conexion.commit(); return True
        except pymysql.MySQLError:
            conexion.rollback(); print("[ERROR] No se pudo eliminar el administrador."); return False
        finally: conexion.close()
