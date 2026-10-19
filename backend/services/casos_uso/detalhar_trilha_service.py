from repositories.trilha_repository import TrilhaRepository
from models.trilha_model import Trilha

class DetalharTrilhaService:
    def __init__(self, repository=None):
        self.repository = repository or TrilhaRepository()

    def executar(self, id_trilha):
        trilha = Trilha.buscar_por_id(id_trilha)
        if not trilha:
            raise ValueError("trilha não encontrada")
        return trilha
