from repositories.checklist_repository import ChecklistRepository


class ChecklistService:
    """Caso de leitura do checklist de equipamentos de uma trilha."""

    def __init__(self):
        self.repository = ChecklistRepository()

    def listar_por_trilha(self, id_trilha):
        return self.repository.listar_por_trilha(id_trilha)
