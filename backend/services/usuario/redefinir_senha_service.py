from datetime import datetime, timezone
import hashlib

from models.token_recuperacao_model import TokenRecuperacao
from models.usuario_model import Usuario
from utils.auth import hash_senha
from utils.excecoes import ErroDeValidacao, RecursoNaoEncontrado


class RedefinirSenhaService:
    def __init__(self, modelo_usuario=None, modelo_token=None):
        self.modelo_usuario = modelo_usuario or Usuario
        self.modelo_token = modelo_token or TokenRecuperacao

    def executar(self, token, nova_senha):
        if not token:
            raise RecursoNaoEncontrado("token inválido ou expirado")
        if not nova_senha or len(nova_senha) < 6:
            raise ErroDeValidacao("a nova senha deve ter pelo menos 6 caracteres")
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        registro = self.modelo_token.buscar_por_hash(token_hash)
        agora = datetime.now(timezone.utc).replace(tzinfo=None)
        if registro is None or registro.usadoEm is not None or registro.expiraEm <= agora:
            raise RecursoNaoEncontrado("token inválido ou expirado")
        usuario = self.modelo_usuario.buscar_por_id(registro.idUsuario)
        if usuario is None:
            raise RecursoNaoEncontrado("usuário não encontrado")
        usuario.senha = hash_senha(nova_senha)
        registro.usadoEm = agora
        usuario.atualizar()
        return {"senhaRedefinida": True}
