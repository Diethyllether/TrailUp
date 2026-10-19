from models.usuario_model import Usuario


class ConsultarSessaoService:
    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario

    def executar(self, id_usuario):
        if not id_usuario:
            return None
        usuario = self.modelo_usuario.buscar_por_id(id_usuario)
        return usuario.to_dict() if usuario else None
