from repositories.checklist_repository import ChecklistRepository


class ConsultarChecklistService:
    def __init__(self, repository=None):
        self.repository = repository or ChecklistRepository()

    def executar(self, id_usuario, id_trilha):
        linhas = self.repository.listar_marcados(id_usuario, id_trilha)
        return {
            "itens": {
                str(linha["idChecklistItem"]): bool(linha["marcado"])
                for linha in linhas
            }
        }
