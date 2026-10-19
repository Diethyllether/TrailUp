from models.checklist_item_model import ChecklistItem


class ChecklistService:
    """Caso de leitura do checklist de equipamentos de uma trilha."""

    def __init__(self):
        pass

    def listar_por_trilha(self, id_trilha):
        return ChecklistItem.query.filter_by(idTrilha=id_trilha).order_by(
            ChecklistItem.obrigatorio.desc(), ChecklistItem.idChecklistItem.asc()
        ).all()
