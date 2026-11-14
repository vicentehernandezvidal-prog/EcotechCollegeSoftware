# conexion.py

# PARA CONECTAR A LAS VARIABLES DE ENTORNO
import os 
from dotenv import load_dotenv

# para cargar variables de archivo .env
load_dotenv()


# manejo de falta de librerias
try:
    import pymysql
except ModuleNotFoundError:
    pymysql = None

# para llamar a la conexion
class Conexion:

    @staticmethod
    def conectar():
        if pymysql is None:
            print("\n ERROR No se pudo importar pymysql.")
            print(" Instala la dependencia con: pip install pymysql")
            return None

        try:
            conexion = pymysql.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 3306)), 
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "ecotech")
            )
            return conexion


        except pymysql.OperationalError:
            # Si MySQL o XAMPP están apagados, captura el error para que el programa no se caiga
            print("\n ERROR No se pudo conectar a la base de datos MySQL.")
            print(" Verifica que el servicio MySQL en XAMPP esté encendido.")
            return None
 