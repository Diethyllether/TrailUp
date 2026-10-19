
from models.usuario_model import Usuario
from services.casos_uso import (
    AtualizarPerfilService,
    CadastrarUsuarioService,
    LoginUsuarioService,
)

class UsuarioService:
    """Facade para fluxos legados; os casos avaliados possuem Services próprios."""

    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario
        self.cadastrar_service = CadastrarUsuarioService(self.modelo_usuario)
        self.login_service = LoginUsuarioService(self.modelo_usuario)
        self.atualizar_perfil_service = AtualizarPerfilService(self.modelo_usuario)

    def cadastrar(self, dados):
        return self.cadastrar_service.executar(dados)

    def login(self, email, senha):
        return self.login_service.executar(email, senha)

    def listar_todos(self):
        return self.modelo_usuario.listar_todos()

    def buscar_por_id(self, id_usuario):
        usuario = self.modelo_usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError("usuário não encontrado")
        return usuario

    def atualizar_perfil(self, id_usuario, dados):
        return self.atualizar_perfil_service.executar(id_usuario, dados)

    def deletar(self, id_usuario):
        usuario = self.buscar_por_id(id_usuario)
        usuario.deletar()
