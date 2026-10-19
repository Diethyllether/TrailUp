from repositories.historico_repository import HistoricoRepository


class ConsultarHistoricoService:
    def __init__(self, repository=None):
        self.repository = repository or HistoricoRepository()

    def executar(self, id_usuario):
        return self.repository.listar_por_usuario(id_usuario)
