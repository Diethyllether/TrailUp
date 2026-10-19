from models.favorito_model import Favorito

class ListarFavoritosService:
    def __init__(self, repository=None):
        self.repository = repository

    def executar(self, id_usuario):
        return Favorito.listar_por_usuario(id_usuario)
