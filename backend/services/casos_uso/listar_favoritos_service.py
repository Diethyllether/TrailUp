from repositories.favorito_repository import FavoritoRepository

class ListarFavoritosService:
    def __init__(self):
        self.repository = FavoritoRepository()

    def executar(self, id_usuario):
        return self.repository.listar_por_usuario(id_usuario)
