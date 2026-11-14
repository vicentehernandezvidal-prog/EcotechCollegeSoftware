import pymysql
from database.conexion import Conexion

class BaseRepository:
    def _ejecutar(self, sql, parametros=(), fetch=False):
        conexion = Conexion.conectar()
        if conexion is None: return [] if fetch else False
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, parametros)
                resultado = cursor.fetchall() if fetch else cursor.rowcount
            if not fetch: conexion.commit()
            return resultado if fetch else resultado >= 0
        except pymysql.MySQLError:
            conexion.rollback()
            print("[ERROR] No se pudo completar la operación en la base de datos.")
            return [] if fetch else False
        finally:
            conexion.close()
