from extensions import db

class Checkpoint(db.Model):
    __tablename__ = "checkpoint"

    idCheckpoint = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    horario = db.Column(db.DateTime, nullable=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idCheckpoint": self.idCheckpoint,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "horario": self.horario.isoformat() if self.horario else None,
            "idTrilha": self.idTrilha,
        }
