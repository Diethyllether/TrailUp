from repositories.relatorio_repository import RelatorioRepository
from utils.excecoes import RecursoNaoEncontrado


class ResumoUsuarioService:
    def __init__(self, repository=None):
        self.repository = repository or RelatorioRepository()

    def executar(self, id_usuario):
        resumo = self.repository.resumo_usuario(id_usuario)
        if not resumo:
            raise RecursoNaoEncontrado("usuário não encontrado")
        return resumo
