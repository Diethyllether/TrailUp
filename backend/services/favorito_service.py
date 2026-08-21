from services.casos_uso import (
    AdicionarFavoritoService,
    ListarFavoritosService,
    RemoverFavoritoService,
)

class FavoritoService:
    """Facade compatível com as rotas antigas, delegando a casos de uso únicos."""

    def __init__(self):
        self.listar_service = ListarFavoritosService()
        self.adicionar_service = AdicionarFavoritoService()
        self.remover_service = RemoverFavoritoService()

    def listar_por_usuario(self, id_usuario):
        return self.listar_service.executar(id_usuario)

    def adicionar(self, id_usuario, id_trilha):
        return self.adicionar_service.executar(id_usuario, id_trilha)

    def remover(self, id_usuario, id_trilha):
        return self.remover_service.executar(id_usuario, id_trilha)
