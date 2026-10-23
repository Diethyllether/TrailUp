"""Extensões compartilhadas pela aplicação Flask."""

from flask_sqlalchemy import SQLAlchemy


class Database:
    """Provedor Singleton da extensão SQLAlchemy da aplicação.

    Flask-SQLAlchemy mantém engines e sessões por aplicação/contexto. Esta
    classe garante que a extensão seja criada uma única vez e reutilizada
    pelas factories, models, repositories e demais módulos.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._db = SQLAlchemy()
        return cls._instance

    @property
    def db(self):
        """Retorna a instância única do Flask-SQLAlchemy."""
        return self._db


# Mantém a interface usada em todo o projeto, enquanto a criação fica
# centralizada no Singleton Database.
database = Database()
db = database.db
