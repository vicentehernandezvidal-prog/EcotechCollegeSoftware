from repositorios.base_repository import BaseRepository

class InformeRepository(BaseRepository):
    def guardar(self, tipo, formato, id_admin):
        if formato not in ("PDF", "EXCEL"): return False
        return self._ejecutar("INSERT INTO INFORME (tipo_contenido,formato,id_admin,fecha_generacion) VALUES (%s,%s,%s,NOW())", (tipo,formato,id_admin))
    def listar(self): return self._ejecutar("SELECT id_informe,tipo_contenido,formato,id_admin,fecha_generacion FROM INFORME ORDER BY fecha_generacion DESC", fetch=True)
    def eliminar(self, id_informe): return self._ejecutar("DELETE FROM INFORME WHERE id_informe=%s", (id_informe,))
