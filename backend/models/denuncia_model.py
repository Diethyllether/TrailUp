from extensions import db

class Denuncia(db.Model):
    __tablename__ = "denuncia"

    idDenuncia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text, nullable=False)
    dataEnvio = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="PENDENTE")
    categoria = db.Column(db.String(30), nullable=False, default="EVENTO")
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), nullable=True)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=True)
    idUsuarioDenunciante = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idUsuarioDenunciado = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=True)

    def to_dict(self):
        return {
            "idDenuncia": self.idDenuncia,
            "descricao": self.descricao,
            "dataEnvio": self.dataEnvio.isoformat() if self.dataEnvio else None,
            "status": self.status,
            "categoria": self.categoria,
            "idEvento": self.idEvento,
            "idTrilha": self.idTrilha,
            "idUsuarioDenunciante": self.idUsuarioDenunciante,
            "idUsuarioDenunciado": self.idUsuarioDenunciado,
        }
