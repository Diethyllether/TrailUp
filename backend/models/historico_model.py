from extensions import db
from models.crud import CrudMixin

class HistoricoTrilha(CrudMixin, db.Model):
    __tablename__ = "historicoTrilha"

    idHistorico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataRealizacao = db.Column(db.Date, nullable=True)
    tempo = db.Column(db.Float, nullable=True)
    avaliacaoPessoal = db.Column(db.Integer, nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), nullable=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idHistorico": self.idHistorico,
            "dataRealizacao": self.dataRealizacao.isoformat() if self.dataRealizacao else None,
            "tempo": self.tempo,
            "avaliacaoPessoal": self.avaliacaoPessoal,
            "idUsuario": self.idUsuario,
            "idEvento": self.idEvento,
            "idTrilha": self.idTrilha,
        }
