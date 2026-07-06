from extensions import db

class Foto(db.Model):
    __tablename__ = "foto"

    idFoto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=True)
    legenda = db.Column(db.String(255), nullable=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idFoto": self.idFoto,
            "url": self.url,
            "legenda": self.legenda,
            "idTrilha": self.idTrilha,
        }
