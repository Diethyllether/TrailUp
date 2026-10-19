from models.usuario_model import Usuario
from utils.auth import hash_senha
from utils.excecoes import ConflitoDeDados, ErroDeValidacao, RecursoNaoEncontrado


class AtualizarPerfilService:
    def __init__(self, modelo_usuario=None):
        self.modelo_usuario = modelo_usuario or Usuario

    def executar(self, id_usuario, dados):
        usuario = self.modelo_usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise RecursoNaoEncontrado("usuário não encontrado")
        if "nome" in dados:
            nome = (dados["nome"] or "").strip()
            if not nome:
                raise ErroDeValidacao("nome não pode ficar vazio")
            usuario.nome = nome
        if "email" in dados:
            email = (dados["email"] or "").strip()
            if not email or "@" not in email:
                raise ErroDeValidacao("informe um e-mail válido")
            existente = self.modelo_usuario.buscar_por_email(email)
            if existente and existente.idUsuario != usuario.idUsuario:
                raise ConflitoDeDados("email já está em uso por outro usuário")
            usuario.email = email
        if "fotoPerfil" in dados:
            usuario.fotoPerfil = dados["fotoPerfil"]
        if dados.get("senha"):
            usuario.senha = hash_senha(dados["senha"])
        return usuario.atualizar().to_dict()
