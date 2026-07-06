import datetime
import secrets

from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.auth import hash_senha, verificar_senha, gerar_token

class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()
        self._tokens_recuperacao = {}

    def cadastrar(self, dados):
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
        self.repository.criar(usuario)
        return usuario

    def login(self, email, senha):
        usuario = self.repository.buscar_por_email(email)
        if not usuario or not verificar_senha(senha, usuario.senha):
            raise ValueError("email ou senha inválidos")

        token = gerar_token(usuario.idUsuario)
        return token, usuario

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

        usuario = self.repository.buscar_por_id(info["idUsuario"])
        if not usuario:
            raise ValueError("usuário não encontrado")

        usuario.senha = hash_senha(nova_senha)
        self.repository.atualizar()
        del self._tokens_recuperacao[token]
        return usuario

    def listar_todos(self):
        return self.repository.listar_todos()

    def buscar_por_id(self, id_usuario):
        usuario = self.repository.buscar_por_id(id_usuario)
        if not usuario:
            raise ValueError("usuário não encontrado")
        return usuario

    def atualizar_perfil(self, id_usuario, dados):
        usuario = self.buscar_por_id(id_usuario)

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

        self.repository.atualizar()
        return usuario

    def deletar(self, id_usuario):
        usuario = self.buscar_por_id(id_usuario)
        self.repository.deletar(usuario)
