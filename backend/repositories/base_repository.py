from extensions import db

class BaseRepository:
    """
    Repository genérico: concentra as operações de acesso a dados que se
    repetem em todas as entidades (listar, buscar por id, criar, atualizar,
    deletar). Cada repository específico herda desta classe e define seu
    `model`, além de métodos de consulta próprios quando necessário.
    """

    model = None

    def listar_todos(self):
        return self.model.query.all()

    def buscar_por_id(self, id_):
        return self.model.query.get(id_)

    def criar(self, instancia):
        db.session.add(instancia)
        db.session.commit()
        return instancia

    def atualizar(self):
        db.session.commit()

    def deletar(self, instancia):
        db.session.delete(instancia)
        db.session.commit()
