from extensions import db
from models.crud import CrudMixin


class TokenRecuperacao(CrudMixin, db.Model):
    __tablename__ = "token_recuperacao"

    idToken = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    tokenHash = db.Column(db.String(64), nullable=False, unique=True)
    expiraEm = db.Column(db.DateTime, nullable=False)
    usadoEm = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "idToken": self.idToken,
            "idUsuario": self.idUsuario,
            "expiraEm": self.expiraEm.isoformat() if self.expiraEm else None,
            "usadoEm": self.usadoEm.isoformat() if self.usadoEm else None,
        }
