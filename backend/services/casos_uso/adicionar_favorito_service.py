import datetime

from models.favorito_model import Favorito

class AdicionarFavoritoService:
    def __init__(self, repository=None):
        self.repository = repository

    def executar(self, id_usuario, id_trilha):
        existente = Favorito.query.filter_by(idUsuario=id_usuario, idTrilha=id_trilha).first()
        if existente:
            return existente

        favorito = Favorito(
            idUsuario=id_usuario,
            idTrilha=id_trilha,
            dataSalvo=datetime.date.today(),
        )
        return favorito.salvar()
