from repositorios.base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
    def crear(self, nombre_usuario, hash_password, correo, rol):
        return self._ejecutar("INSERT INTO USUARIO (nombre_usuario, hash_password, correo, rol) VALUES (%s,%s,%s,%s)", #%s placeholders
                              (nombre_usuario, hash_password, correo, rol))
    def buscar_login(self, nombre_usuario):
        filas = self._ejecutar("SELECT id_usuario,nombre_usuario,hash_password,correo,rol FROM USUARIO WHERE nombre_usuario=%s", (nombre_usuario,), True)
        return filas[0] if filas else None
    def listar(self):
        return self._ejecutar("SELECT id_usuario,nombre_usuario,correo,rol FROM USUARIO ORDER BY id_usuario", fetch=True)
    def actualizar(self, id_usuario, nombre_usuario, correo):
        return self._ejecutar("UPDATE USUARIO SET nombre_usuario=%s, correo=%s WHERE id_usuario=%s", (nombre_usuario, correo, id_usuario))
    def eliminar(self, id_usuario):
        return self._ejecutar("DELETE FROM USUARIO WHERE id_usuario=%s", (id_usuario,))
