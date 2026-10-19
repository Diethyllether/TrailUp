from extensions import db
from models.crud import CrudMixin


class EventoTrilha(CrudMixin, db.Model):
    __tablename__ = "evento_trilha"

    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), primary_key=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), primary_key=True)

    def to_dict(self):
        return {"idEvento": self.idEvento, "idTrilha": self.idTrilha}
