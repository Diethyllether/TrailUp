from models.checklist_item_model import ChecklistItem


class ChecklistService:
    """Caso de leitura do checklist de equipamentos de uma trilha."""

    def __init__(self):
        pass

    def listar_por_trilha(self, id_trilha):
        return ChecklistItem.listar_por_trilha(id_trilha)
