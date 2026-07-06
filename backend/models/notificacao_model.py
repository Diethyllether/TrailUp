from extensions import db

class Notificacao(db.Model):
    __tablename__ = "notificacao"

    idNotificacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensagem = db.Column(db.Text, nullable=True)
    dataEnvio = db.Column(db.DateTime, nullable=True)
    lida = db.Column(db.Boolean, default=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idEvento = db.Column(db.Integer, db.ForeignKey("evento.idEvento"), nullable=True)

    def to_dict(self):
        return {
            "idNotificacao": self.idNotificacao,
            "mensagem": self.mensagem,
            "dataEnvio": self.dataEnvio.isoformat() if self.dataEnvio else None,
            "lida": self.lida,
            "idUsuario": self.idUsuario,
            "idEvento": self.idEvento,
        }
