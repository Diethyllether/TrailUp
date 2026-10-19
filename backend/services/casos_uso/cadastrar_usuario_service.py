import datetime

from models.usuario_model import Usuario
from utils.auth import hash_senha

class CadastrarUsuarioService:
    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario

    def executar(self, dados):
        if not dados.get("nome") or not dados.get("email") or not dados.get("senha"):
            raise ValueError("nome, email e senha são obrigatórios")
        if dados.get("aceitouTermo") is not True:
            raise ValueError("é necessário aceitar o Termo de Consentimento")

        if self.modelo_usuario.buscar_por_email(dados["email"]):
            raise ValueError("já existe um usuário cadastrado com este email")

        usuario = self.modelo_usuario(
            nome=dados["nome"],
            email=dados["email"],
            senha=hash_senha(dados["senha"]),
            fotoPerfil=dados.get("fotoPerfil"),
            dataCadastro=datetime.date.today(),
            termoAceitoEm=datetime.datetime.now(),
            versaoTermo="1.0",
        )
        return usuario.salvar()
