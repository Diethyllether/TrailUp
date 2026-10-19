from extensions import db
from models.crud import CrudMixin

class Avaliacao(CrudMixin, db.Model):
    __tablename__ = "avaliacao"

    idAvaliacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    data = db.Column(db.Date, nullable=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey("usuario.idUsuario"), nullable=False)
    idTrilha = db.Column(db.Integer, db.ForeignKey("trilha.idTrilha"), nullable=False)

    @classmethod
    def listar_por_trilha(cls, id_trilha):
        return cls.query.filter_by(idTrilha=id_trilha).all()

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        return cls.query.filter_by(idUsuario=id_usuario).all()

    def to_dict(self):
        return {
            "idAvaliacao": self.idAvaliacao,
            "nota": self.nota,
            "comentario": self.comentario,
            "data": self.data.isoformat() if self.data else None,
            "idUsuario": self.idUsuario,
            "idTrilha": self.idTrilha,
        }
