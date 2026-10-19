from extensions import db
from models.crud import CrudMixin


class ParticipanteEvento(CrudMixin, db.Model):
    __tablename__ = "participante_evento"

    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), primary_key=True)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), primary_key=True)

    def to_dict(self):
        return {"idUsuario": self.idUsuario, "idEvento": self.idEvento}

