import datetime
import secrets

from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.casos_uso import (
    AtualizarPerfilService,
    CadastrarUsuarioService,
    LoginUsuarioService,
)
from utils.auth import hash_senha

class UsuarioService:
    """Facade para fluxos legados; os casos avaliados possuem Services próprios."""

    def __init__(self):
        self.repository = UsuarioRepository()
        self.cadastrar_service = CadastrarUsuarioService()
        self.login_service = LoginUsuarioService()
        self.atualizar_perfil_service = AtualizarPerfilService()
        self._tokens_recuperacao = {}

    def cadastrar(self, dados):
        return self.cadastrar_service.executar(dados)

    def login(self, email, senha):
        return self.login_service.executar(email, senha)

    def solicitar_recuperacao_senha(self, email):
        usuario = self.repository.buscar_por_email(email)
        if not usuario:
            return None
        token = secrets.token_urlsafe(32)
        self._tokens_recuperacao[token] = {
            "idUsuario": usuario.idUsuario,
            "expira": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }
        return token

    def redefinir_senha(self, token, nova_senha):
        info = self._tokens_recuperacao.get(token)
        if not info or info["expira"] < datetime.datetime.utcnow():
            raise ValueError("token de recuperação inválido ou expirado")

        usuario = Usuario.buscar_por_id(info["idUsuario"])
        if not usuario:
            raise ValueError("usuário não encontrado")

        usuario.senha = hash_senha(nova_senha)
        usuario.atualizar()
        del self._tokens_recuperacao[token]
        return usuario

    def listar_todos(self):
        return Usuario.listar_todos()

    def buscar_por_id(self, id_usuario):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError("usuário não encontrado")
        return usuario

    def atualizar_perfil(self, id_usuario, dados):
        return self.atualizar_perfil_service.executar(id_usuario, dados)

    def deletar(self, id_usuario):
        usuario = self.buscar_por_id(id_usuario)
        usuario.deletar()
