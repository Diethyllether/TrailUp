from extensions import db


class ChecklistItem(db.Model):
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

    def to_dict(self):
        return {
            "idChecklistItem": self.idChecklistItem,
            "descricao": self.descricao,
            "obrigatorio": self.obrigatorio,
            "idTrilha": self.idTrilha,
        }
