class RegistroTiempo:
    def __init__(self, id_registro, id_empleado, id_proyecto, horas, descripcion_tarea,
                 estado_validacion="PENDIENTE", fecha=None):
        self.__id_registro = id_registro
        self.__id_empleado = id_empleado
        self.__id_proyecto = id_proyecto
        self.__horas = horas
        self.__descripcion_tarea = descripcion_tarea
        self.__estado_validacion = estado_validacion
        self.__fecha = fecha
    def get_id_registro(self): return self.__id_registro
    def get_id_empleado(self): return self.__id_empleado
    def get_id_proyecto(self): return self.__id_proyecto
    def get_horas(self): return self.__horas
    def get_descripcion_tarea(self): return self.__descripcion_tarea
    def get_estado_validacion(self): return self.__estado_validacion
