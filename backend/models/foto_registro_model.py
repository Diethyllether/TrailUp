from extensions import db
from models.crud import CrudMixin


class FotoRegistro(CrudMixin, db.Model):
    __tablename__ = "fotoRegistro"

    idFotoRegistro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=True)
    legenda = db.Column(db.String(255), nullable=True)
    idRegistro = db.Column(db.Integer, db.ForeignKey("registroRealizado.idRegistro"), nullable=False)

    def to_dict(self):
        return {
            "idFotoRegistro": self.idFotoRegistro,
            "url": self.url,
            "legenda": self.legenda,
            "idRegistro": self.idRegistro,
        }
