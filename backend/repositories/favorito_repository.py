from models.favorito_model import Favorito

class FavoritoRepository:
    """Consultas por chave composta/usuário. Persistência simples fica na Model."""

    def listar_por_usuario(self, id_usuario):
        return Favorito.query.filter_by(idUsuario=id_usuario).all()

    def buscar(self, id_usuario, id_trilha):
        return Favorito.query.filter_by(idUsuario=id_usuario, idTrilha=id_trilha).first()
