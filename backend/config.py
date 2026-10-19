"""Configuração da aplicação carregada de variáveis de ambiente."""

import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:8000")
    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8000")

    @classmethod
    def validar(cls):
        """Falha cedo quando segredos ou conexão não foram configurados."""
        ausentes = []
        if not cls.SECRET_KEY:
            ausentes.append("SECRET_KEY")
        if not cls.SQLALCHEMY_DATABASE_URI:
            ausentes.append("DATABASE_URL")
        if ausentes:
            nomes = ", ".join(ausentes)
            raise RuntimeError(
                f"Configuração obrigatória ausente: {nomes}. "
                "Defina as variáveis de ambiente ou configure o arquivo .env."
            )
