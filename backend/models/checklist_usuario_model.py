from extensions import db
from models.crud import CrudMixin


class ChecklistUsuario(CrudMixin, db.Model):
    __tablename__ = "checklist_usuario"

    idUsuario = db.Column(
        db.Integer, db.ForeignKey("usuario.idUsuario", ondelete="CASCADE"), primary_key=True
    )
    idChecklistItem = db.Column(
        db.Integer,
        db.ForeignKey("checklist_item.idChecklistItem", ondelete="CASCADE"),
        primary_key=True,
    )
    marcado = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def buscar(cls, id_usuario, id_item):
        return db.session.get(cls, (id_usuario, id_item))

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        return cls.query.filter_by(idUsuario=id_usuario).all()

    def to_dict(self):
        return {
            "idUsuario": self.idUsuario,
            "idChecklistItem": self.idChecklistItem,
            "marcado": self.marcado,
        }
