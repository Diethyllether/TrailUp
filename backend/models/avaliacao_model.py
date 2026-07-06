from extensions import db

class Avaliacao(db.Model):
    __tablename__ = "avaliacao"

    idAvaliacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    data = db.Column(db.Date, nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    def to_dict(self):
        return {
            "idAvaliacao": self.idAvaliacao,
            "nota": self.nota,
            "comentario": self.comentario,
            "data": self.data.isoformat() if self.data else None,
            "idUsuario": self.idUsuario,
            "idTrilha": self.idTrilha,
        }
