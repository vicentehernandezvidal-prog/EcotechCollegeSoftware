class Informe:
    def __init__(self, id_informe, tipo_contenido, formato, id_admin=None, fecha_generacion=None):
        self.__id_informe = id_informe
        self.__tipo_contenido = tipo_contenido
        self.__formato = formato
        self.__id_admin = id_admin
        self.__fecha_generacion = fecha_generacion
    def get_id_informe(self): return self.__id_informe
    def get_tipo_contenido(self): return self.__tipo_contenido
    def get_formato(self): return self.__formato
    def get_id_admin(self): return self.__id_admin
