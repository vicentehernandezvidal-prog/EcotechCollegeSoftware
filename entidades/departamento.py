class Departamento:
    def __init__(self, id_departamento, nombre_dept, id_gerente=None):
        self.__id_departamento = id_departamento
        self.__nombre_dept = nombre_dept
        self.__id_gerente = id_gerente
    def get_id_departamento(self): return self.__id_departamento
    def get_nombre_dept(self): return self.__nombre_dept
    def get_id_gerente(self): return self.__id_gerente
