class Sesion:
    """Estado global de la sesion activa."""
    usuario = None        # UsuarioDTO
    tipo = None           # 'Administrador' | 'Tradicional' | 'Esporadico'
    id_bitacora = None

    @classmethod
    def iniciar(cls, usuario, tipo, id_bitacora):
        cls.usuario, cls.tipo, cls.id_bitacora = usuario, tipo, id_bitacora

    @classmethod
    def cerrar(cls):
        cls.usuario = cls.tipo = cls.id_bitacora = None
