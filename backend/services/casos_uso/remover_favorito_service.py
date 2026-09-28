from repositories.favorito_repository import FavoritoRepository

class RemoverFavoritoService:
    def __init__(self, repository=None):
        self.repository = repository or FavoritoRepository()

    def executar(self, id_usuario, id_trilha):
        favorito = self.repository.buscar(id_usuario, id_trilha)
        if not favorito:
            raise ValueError("trilha não está nos favoritos deste usuário")
        self.repository.deletar(favorito)
