from services.casos_uso import (
    AdicionarFavoritoService,
    ListarFavoritosService,
    RemoverFavoritoService,
)
from repositories.favorito_repository import FavoritoRepository

class FavoritoService:
    """Facade compatível com as rotas antigas, delegando a casos de uso únicos."""

    def __init__(self, repository=None):
        repository = repository or FavoritoRepository()
        self.listar_service = ListarFavoritosService(repository)
        self.adicionar_service = AdicionarFavoritoService(repository)
        self.remover_service = RemoverFavoritoService(repository)

    def listar_por_usuario(self, id_usuario):
        return self.listar_service.executar(id_usuario)

    def adicionar(self, id_usuario, id_trilha):
        return self.adicionar_service.executar(id_usuario, id_trilha)

    def remover(self, id_usuario, id_trilha):
        return self.remover_service.executar(id_usuario, id_trilha)
