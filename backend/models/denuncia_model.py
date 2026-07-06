from extensions import db

class Denuncia(db.Model):
    __tablename__ = "denuncia"

    idDenuncia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text, nullable=True)
    dataEnvio = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="PENDENTE")
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), nullable=False)
    idUsuarioDenunciante = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idUsuarioDenunciado = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=True)

    def to_dict(self):
        return {
            "idDenuncia": self.idDenuncia,
            "descricao": self.descricao,
            "dataEnvio": self.dataEnvio.isoformat() if self.dataEnvio else None,
            "status": self.status,
            "idEvento": self.idEvento,
            "idUsuarioDenunciante": self.idUsuarioDenunciante,
            "idUsuarioDenunciado": self.idUsuarioDenunciado,
        }
