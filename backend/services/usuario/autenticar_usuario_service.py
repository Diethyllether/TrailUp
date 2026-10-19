from models.usuario_model import Usuario
from utils.auth import verificar_senha
from utils.excecoes import NaoAutenticado


class AutenticarUsuarioService:
    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario

    def executar(self, email, senha):
        usuario = self.modelo_usuario.buscar_por_email((email or "").strip())
        if not usuario or not verificar_senha(senha or "", usuario.senha):
            raise NaoAutenticado("email ou senha inválidos")
        return usuario.to_dict()
