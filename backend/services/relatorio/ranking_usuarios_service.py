from repositories.relatorio_repository import RelatorioRepository
from utils.excecoes import ErroDeValidacao


class RankingUsuariosService:
    def __init__(self, repository=None):
        self.repository = repository or RelatorioRepository()

    def executar(self, limite=10):
        try:
            limite = int(limite)
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("limite deve ser um número inteiro") from error
        if not 1 <= limite <= 100:
            raise ErroDeValidacao("limite deve estar entre 1 e 100")
        return self.repository.ranking_usuarios(limite)
