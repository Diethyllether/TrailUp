"""Adapter SMTP para envio de mensagens da aplicação."""

from email.message import EmailMessage
import os
import smtplib


class EnviarEmailService:
    def executar(self, destinatario, assunto, conteudo):
        host = os.environ.get("SMTP_HOST")
        if not host:
            raise RuntimeError("SMTP_HOST não está configurado")

        mensagem = EmailMessage()
        mensagem["Subject"] = assunto
        mensagem["From"] = os.environ.get(
            "SMTP_FROM", os.environ.get("SMTP_USER", "trailup@localhost")
        )
        mensagem["To"] = destinatario
        mensagem.set_content(conteudo)

        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=10) as smtp:
            smtp.starttls()
            usuario = os.environ.get("SMTP_USER")
            if usuario:
                smtp.login(usuario, os.environ.get("SMTP_PASSWORD", ""))
            smtp.send_message(mensagem)
        return {"enviado": True}
