import datetime

from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.auth import hash_senha

class CadastrarUsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, dados):
        if not dados.get("nome") or not dados.get("email") or not dados.get("senha"):
            raise ValueError("nome, email e senha são obrigatórios")

        if self.repository.buscar_por_email(dados["email"]):
            raise ValueError("já existe um usuário cadastrado com este email")

        usuario = Usuario(
            nome=dados["nome"],
            email=dados["email"],
            senha=hash_senha(dados["senha"]),
            fotoPerfil=dados.get("fotoPerfil"),
            dataCadastro=datetime.date.today(),
        )
        return usuario.salvar()
