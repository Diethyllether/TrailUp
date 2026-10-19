from models.usuario_model import Usuario
from utils.auth import verificar_senha

class LoginUsuarioService:
    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario

    def executar(self, email, senha):
        usuario = self.modelo_usuario.buscar_por_email(email)
        if not usuario or not verificar_senha(senha, usuario.senha):
            raise ValueError("email ou senha inválidos")

        return usuario
