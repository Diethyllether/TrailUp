from repositories.trilha_repository import TrilhaRepository
from utils.excecoes import ErroDeValidacao


class FiltrarTrilhasService:
    def __init__(self, repository=None):
        self.repository = repository or TrilhaRepository()

    def executar(self, distancia_max=None, duracao_max=None, nota_min=None, ordem=None):
        try:
            distancia = float(distancia_max) if distancia_max not in (None, "") else None
            duracao = float(duracao_max) if duracao_max not in (None, "") else None
            nota = float(nota_min) if nota_min not in (None, "") else None
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("filtros numéricos inválidos") from error
        if ordem not in (None, "", "nome", "nota", "distancia", "duracao"):
            raise ErroDeValidacao("ordenação inválida")
        trilhas = self.repository.listar_ordenadas(
            ordem or None, distancia, duracao, nota
        )
        return [trilha.to_dict() for trilha in trilhas]
