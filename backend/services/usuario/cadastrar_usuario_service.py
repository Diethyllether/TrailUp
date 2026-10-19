import datetime

from models.usuario_model import Usuario
from utils.auth import hash_senha
from utils.excecoes import ConflitoDeDados, ErroDeValidacao


class CadastrarUsuarioService:
    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario

    def executar(self, dados):
        nome = (dados.get("nome") or "").strip()
        email = (dados.get("email") or "").strip()
        senha = dados.get("senha") or ""
        if not nome or not email or not senha:
            raise ErroDeValidacao("nome, email e senha são obrigatórios")
        if dados.get("aceitouTermo") is not True:
            raise ErroDeValidacao("é necessário aceitar o Termo de Consentimento")
        if self.modelo_usuario.buscar_por_email(email):
            raise ConflitoDeDados("já existe um usuário cadastrado com este email")
        usuario = self.modelo_usuario(
            nome=nome, email=email, senha=hash_senha(senha),
            fotoPerfil=dados.get("fotoPerfil"), dataCadastro=datetime.date.today(),
            termoAceitoEm=datetime.datetime.now(), versaoTermo="1.0",
        ).salvar()
        return usuario.to_dict()
