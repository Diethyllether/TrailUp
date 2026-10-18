from repositories.usuario_repository import UsuarioRepository
from utils.auth import hash_senha

class AtualizarPerfilService:
    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()

    def executar(self, id_usuario, dados):
        usuario = self.repository.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError("usuário não encontrado")

        if "nome" in dados:
            nome = (dados["nome"] or "").strip()
            if not nome:
                raise ValueError("nome não pode ficar vazio")
            usuario.nome = nome
        if "email" in dados:
            email = (dados["email"] or "").strip()
            if not email or "@" not in email:
                raise ValueError("informe um e-mail válido")
            existente = self.repository.buscar_por_email(email)
            if existente and existente.idUsuario != usuario.idUsuario:
                raise ValueError("email já está em uso por outro usuário")
            usuario.email = email
        if "fotoPerfil" in dados:
            usuario.fotoPerfil = dados["fotoPerfil"]
        if "senha" in dados and dados["senha"]:
            usuario.senha = hash_senha(dados["senha"])

        self.repository.atualizar()
        return usuario
