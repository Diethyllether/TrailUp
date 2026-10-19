from extensions import db
from models.crud import CrudMixin


class RegistroRealizado(CrudMixin, db.Model):
    __tablename__ = "registroRealizado"

    idRegistro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    horario = db.Column(db.DateTime, nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    idHistorico = db.Column(db.Integer, db.ForeignKey("historicoTrilha.idHistorico"), nullable=False)

    @classmethod
    def listar_por_historico(cls, id_historico):
        return cls.query.filter_by(idHistorico=id_historico).all()

    def to_dict(self):
        return {
            "idRegistro": self.idRegistro,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "horario": self.horario.isoformat() if self.horario else None,
            "observacao": self.observacao,
            "idHistorico": self.idHistorico,
        }
