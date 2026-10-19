"""Operações Active Record compartilhadas pelas entidades ORM."""

from extensions import db


class CrudMixin:
    """CRUD simples disponível diretamente nas Models."""

    def salvar(self):
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, **campos):
        for nome, valor in campos.items():
            if hasattr(self, nome) and valor is not None:
                setattr(self, nome, valor)
        db.session.commit()
        return self

    def deletar(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def listar_todos(cls):
        return cls.query.all()

    @classmethod
    def buscar_por_id(cls, identificador):
        return db.session.get(cls, identificador)
