from datetime import date
from extensions import db

class Favorito(db.Model):
    __tablename__ = "favorito"
    __table_args__ = (db.UniqueConstraint("idUsuario", "idTrilha", name="uq_favorito"),)

    idFavorito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataSalvo = db.Column(db.Date, default=date.today)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idFavorito": self.idFavorito,
            "dataSalvo": self.dataSalvo.isoformat() if self.dataSalvo else None,
            "idUsuario": self.idUsuario,
            "idTrilha": self.idTrilha,
        }
