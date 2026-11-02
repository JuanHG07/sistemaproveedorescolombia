class Sesion:
    usuario = None       
    tipo = None          
    id_bitacora = None   

    @classmethod
    def iniciar(cls, usuario, tipo, id_bitacora):
        cls.usuario, cls.tipo, cls.id_bitacora = usuario, tipo, id_bitacora

    @classmethod
    def cerrar(cls):
        cls.usuario = cls.tipo = cls.id_bitacora = None