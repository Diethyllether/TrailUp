from extensions import db
from models.crud import CrudMixin


class ChecklistItem(CrudMixin, db.Model):
    """Item de equipamento recomendado ou obrigatório para uma trilha."""

    __tablename__ = "checklist_item"

    idChecklistItem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(200), nullable=False)
    obrigatorio = db.Column(db.Boolean, nullable=False, default=False)
    idTrilha = db.Column(
        db.Integer,
        db.ForeignKey("trilha.idTrilha", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    @classmethod
    def listar_por_trilha(cls, id_trilha):
        return cls.query.filter_by(idTrilha=id_trilha).order_by(
            cls.obrigatorio.desc(), cls.idChecklistItem.asc()
        ).all()

    def to_dict(self):
        return {
            "idChecklistItem": self.idChecklistItem,
            "descricao": self.descricao,
            "obrigatorio": self.obrigatorio,
            "idTrilha": self.idTrilha,
        }
