import datetime

from models.favorito_model import Favorito
from repositories.favorito_repository import FavoritoRepository

class FavoritoService:
    def __init__(self):
        self.repository = FavoritoRepository()

    def listar_por_usuario(self, id_usuario):
        return self.repository.listar_por_usuario(id_usuario)

    def adicionar(self, id_usuario, id_trilha):
        existente = self.repository.buscar(id_usuario, id_trilha)
        if existente:
            return existente

        favorito = Favorito(
            idUsuario=id_usuario, idTrilha=id_trilha, dataSalvo=datetime.date.today()
        )
        self.repository.criar(favorito)
        return favorito

    def remover(self, id_usuario, id_trilha):
        favorito = self.repository.buscar(id_usuario, id_trilha)
        if not favorito:
            raise ValueError("trilha não está nos favoritos deste usuário")
        self.repository.deletar(favorito)
