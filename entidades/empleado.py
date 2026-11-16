from entidades.usuario import Usuario

class Empleado(Usuario):
    def __init__(self, id_empleado, id_usuario, nombre_usuario, hash_password, correo,
                 rut, id_departamento, primer_nombre, primer_apellido):
        super().__init__(id_usuario, nombre_usuario, hash_password, correo, "EMPLEADO")
        self.__id_empleado = id_empleado
        self.__rut = rut
        self.__id_departamento = id_departamento
        self.__primer_nombre = primer_nombre
        self.__primer_apellido = primer_apellido

    def get_id_empleado(self): return self.__id_empleado
    def get_rut(self): return self.__rut
    def get_id_departamento(self): return self.__id_departamento
    def get_primer_nombre(self): return self.__primer_nombre
    def get_primer_apellido(self): return self.__primer_apellido

    def autenticar(self, password, password_service):
        return super().autenticar(password, password_service)

    #FUNCION PARA SOLICITAR SALARIO EN OTRAS DIVISAS
    def obtener_salario_cifrado(self, id_empleado):
        sql = "SELECT salario_cifrado FROM EMPLEADO WHERE id_empleado=%s"
        filas = self._ejecutar(sql, (id_empleado,), fetch = True)
        return filas[0][0] if filas else None

    


