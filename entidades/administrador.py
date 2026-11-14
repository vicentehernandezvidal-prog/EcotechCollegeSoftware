from entidades.usuario import Usuario

class Admin(Usuario):
    def __init__(self, id_admin, id_usuario, nombre_usuario, hash_password, correo):
        super().__init__(id_usuario, nombre_usuario, hash_password, correo, "ADMINISTRADOR")
        self.__id_admin = id_admin

    def get_id_admin(self): return self.__id_admin

    def autenticar(self, password, password_service):
        return super().autenticar(password, password_service)
