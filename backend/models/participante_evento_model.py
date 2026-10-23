from extensions import db
from models.crud import CrudMixin


class ParticipanteEvento(CrudMixin, db.Model):
    __tablename__ = "participante_evento"

    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), primary_key=True)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), primary_key=True)

    @classmethod
    def buscar(cls, id_usuario, id_evento):
        return cls.query.filter_by(idUsuario=id_usuario, idEvento=id_evento).first()

    @classmethod
    def listar_por_evento(cls, id_evento):
        return cls.query.filter_by(idEvento=id_evento).all()

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        return cls.query.filter_by(idUsuario=id_usuario).all()

    def to_dict(self):
        return {"idUsuario": self.idUsuario, "idEvento": self.idEvento}

