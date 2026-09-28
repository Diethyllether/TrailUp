from models.favorito_model import Favorito
from repositories.base_repository import BaseRepository

class FavoritoRepository(BaseRepository):
    """Consultas por chave composta/usuário. Persistência simples fica na Model."""

    model = Favorito

    def listar_por_usuario(self, id_usuario):
        return Favorito.query.filter_by(idUsuario=id_usuario).all()

    def buscar(self, id_usuario, id_trilha):
        return Favorito.query.filter_by(idUsuario=id_usuario, idTrilha=id_trilha).first()
