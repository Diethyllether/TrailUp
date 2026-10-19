
from repositories.usuario_repository import UsuarioRepository
from services.casos_uso import (
    AtualizarPerfilService,
    CadastrarUsuarioService,
    LoginUsuarioService,
)

class UsuarioService:
    """Facade para fluxos legados; os casos avaliados possuem Services próprios."""

    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()
        self.cadastrar_service = CadastrarUsuarioService(self.repository)
        self.login_service = LoginUsuarioService(self.repository)
        self.atualizar_perfil_service = AtualizarPerfilService(self.repository)

    def cadastrar(self, dados):
        return self.cadastrar_service.executar(dados)

    def login(self, email, senha):
        return self.login_service.executar(email, senha)

    def listar_todos(self):
        return self.repository.listar_todos()

    def buscar_por_id(self, id_usuario):
        usuario = self.repository.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError("usuário não encontrado")
        return usuario

    def atualizar_perfil(self, id_usuario, dados):
        return self.atualizar_perfil_service.executar(id_usuario, dados)

    def deletar(self, id_usuario):
        usuario = self.buscar_por_id(id_usuario)
        self.repository.deletar(usuario)
