class Usuario:
    """Clase base para las cuentas del sistema EcoTech."""
    def __init__(self, id_usuario, nombre_usuario, hash_password, correo, rol): # CONSTRUCTOR DE LA CLASE
        self._id_usuario = id_usuario
        self._nombre_usuario = nombre_usuario
        self._hash_password = hash_password
        self._correo = correo
        self._rol = rol

# METODOS PARA OBTENER 
    def get_id_usuario(self): return self._id_usuario
    def get_nombre_usuario(self): return self._nombre_usuario
    def get_hash_password(self): return self._hash_password
    def get_correo(self): return self._correo
    def get_rol(self): return self._rol

    def autenticar(self, password, password_service):
        return password_service.verificar(password, self._hash_password)

    def mostrar_datos(self):
        return f"Usuario: {self._nombre_usuario} | Correo: {self._correo} | Rol: {self._rol}"
