from models.checklist_item_model import ChecklistItem


class ChecklistRepository:
    """Consultas dos equipamentos vinculados às trilhas."""

    def listar_por_trilha(self, id_trilha):
        return (
            ChecklistItem.query.filter_by(idTrilha=id_trilha)
            .order_by(ChecklistItem.obrigatorio.desc(), ChecklistItem.idChecklistItem.asc())
            .all()
        )
