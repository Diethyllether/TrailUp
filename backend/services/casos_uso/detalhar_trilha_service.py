from models.trilha_model import Trilha

class DetalharTrilhaService:
    def executar(self, id_trilha):
        trilha = Trilha.buscar_por_id(id_trilha)
        if not trilha:
            raise ValueError("trilha não encontrada")
        return trilha
