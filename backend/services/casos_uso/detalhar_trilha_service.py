from repositories.trilha_repository import TrilhaRepository

class DetalharTrilhaService:
    def __init__(self, repository=None):
        self.repository = repository or TrilhaRepository()

    def executar(self, id_trilha):
        trilha = self.repository.buscar_por_id(id_trilha)
        if not trilha:
            raise ValueError("trilha não encontrada")
        return trilha
