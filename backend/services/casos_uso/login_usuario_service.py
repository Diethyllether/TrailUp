from repositories.usuario_repository import UsuarioRepository
from utils.auth import verificar_senha, gerar_token

class LoginUsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, email, senha):
        usuario = self.repository.buscar_por_email(email)
        if not usuario or not verificar_senha(senha, usuario.senha):
            raise ValueError("email ou senha inválidos")

        return gerar_token(usuario.idUsuario), usuario
