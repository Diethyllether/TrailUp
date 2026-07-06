from models.avaliacao_model import Avaliacao
from repositories.base_repository import BaseRepository

class AvaliacaoRepository(BaseRepository):
    model = Avaliacao

    def listar_por_trilha(self, id_trilha):
        return Avaliacao.query.filter_by(idTrilha=id_trilha).all()

    def listar_por_usuario(self, id_usuario):
        return Avaliacao.query.filter_by(idUsuario=id_usuario).all()
