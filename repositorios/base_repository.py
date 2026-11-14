import pymysql # lib para la db
from database.conexion import Conexion

# repo base para centralizar la conexion en metodo _ejecutar()
class baseRepository: 
    def _ejecutar(self, sql, parametros=(), fetch =False): # FETCH TRUE PARA LEER Y FALSE PARA MODIFICAR 
        conexion = Conexion.conectar()
        if conexion is None: return [] if fetch else False # evitar crasheo del software, devuelve lista vacia en lugar de none 
        try:
            with conexion.cursor() as cursor: #cursor para la consulta
                cursor.execute(sql, parametros) # para leer la consulta sql y separar de los datos
                resultado = cursor.fetchall() if fetch else cursor.rowcount # operador ternario que almacena la consulta de fetch en resultado 
            if not fetch: conexion.commit() # si no se leen los datos se "commitean" 
            return resultado if fetch else resultado >= 0 #return para dsp


# para controlar si la conexion falla y cerrarla 

        except pymysql.MySQLError: 
            conexion.rollback()
            print("[ERROR] No se pudo completar la operación en la base de datos.")
            return [] if fetch else False
        finally: 
            conexion.close()