from repositories.favorito_repository import FavoritoRepository


class ListarFavoritosService:
    def __init__(self, repository=None):
        self.repository = repository or FavoritoRepository()

    def executar(self, id_usuario):
        favoritos = self.repository.listar_por_usuario(id_usuario)
        return [
            {
                **favorito,
                "media": [favorito.get("mediaNota"), favorito.get("quantidadeAvaliacoes", 0)],
                "favorito": True,
            }
            for favorito in favoritos
        ]
