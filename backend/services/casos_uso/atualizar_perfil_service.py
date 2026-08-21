from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.auth import hash_senha

class AtualizarPerfilService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, id_usuario, dados):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError("usuário não encontrado")

        if "nome" in dados:
            usuario.nome = dados["nome"]
        if "email" in dados:
            existente = self.repository.buscar_por_email(dados["email"])
            if existente and existente.idUsuario != usuario.idUsuario:
                raise ValueError("email já está em uso por outro usuário")
            usuario.email = dados["email"]
        if "fotoPerfil" in dados:
            usuario.fotoPerfil = dados["fotoPerfil"]
        if "senha" in dados and dados["senha"]:
            usuario.senha = hash_senha(dados["senha"])

        return usuario.atualizar()
