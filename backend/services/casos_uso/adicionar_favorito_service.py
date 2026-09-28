import datetime

from models.favorito_model import Favorito
from repositories.favorito_repository import FavoritoRepository

class AdicionarFavoritoService:
    def __init__(self, repository=None):
        self.repository = repository or FavoritoRepository()

    def executar(self, id_usuario, id_trilha):
        existente = self.repository.buscar(id_usuario, id_trilha)
        if existente:
            return existente

        favorito = Favorito(
            idUsuario=id_usuario,
            idTrilha=id_trilha,
            dataSalvo=datetime.date.today(),
        )
        return self.repository.criar(favorito)
