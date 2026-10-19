from datetime import datetime, timedelta, timezone
import hashlib
import logging
import os
import secrets
import smtplib

from models.token_recuperacao_model import TokenRecuperacao
from models.usuario_model import Usuario
from services.externos.enviar_email_service import EnviarEmailService


class SolicitarRecuperacaoSenhaService:
    def __init__(self, modelo_usuario=None, modelo_token=None, email_service=None):
        self.modelo_usuario = modelo_usuario or Usuario
        self.modelo_token = modelo_token or TokenRecuperacao
        self.email_service = email_service or EnviarEmailService()

    def executar(self, email):
        usuario = self.modelo_usuario.buscar_por_email((email or "").strip())
        if usuario is None:
            return {"solicitacaoIniciada": True}

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self.modelo_token(
            idUsuario=usuario.idUsuario,
            tokenHash=token_hash,
            expiraEm=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=1),
        ).salvar()

        link = (
            f"{os.environ.get('FRONTEND_URL', 'http://localhost:8000')}"
            f"/?page=reset-password&token={token}"
        )
        try:
            self.email_service.executar(
                usuario.email,
                "Recuperação de senha TrailUp",
                f"Para redefinir sua senha, acesse: {link}\nO link expira em 1 hora.",
            )
        except (OSError, RuntimeError, ValueError, smtplib.SMTPException) as erro:
            # Não devolve o token ao cliente nem revela se o e-mail existe.
            logging.getLogger(__name__).warning(
                "Não foi possível enviar e-mail de recuperação (%s)",
                type(erro).__name__,
            )
        return {"solicitacaoIniciada": True}
