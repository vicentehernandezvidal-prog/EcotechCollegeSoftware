class Proyecto:
    def __init__(self, id_proyecto, nombre, descripcion, fecha_inicio=None):
        self.__id_proyecto = id_proyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
    def get_id_proyecto(self): return self.__id_proyecto
    def get_nombre(self): return self.__nombre
    def get_descripcion(self): return self.__descripcion
    def get_fecha_inicio(self): return self.__fecha_inicio
