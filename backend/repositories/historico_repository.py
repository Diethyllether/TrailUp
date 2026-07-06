from models.historico_model import HistoricoTrilha, RegistroRealizado, FotoRegistro
from repositories.base_repository import BaseRepository

class HistoricoRepository(BaseRepository):
    model = HistoricoTrilha

    def listar_por_usuario(self, id_usuario):
        return HistoricoTrilha.query.filter_by(idUsuario=id_usuario).all()

class RegistroRealizadoRepository(BaseRepository):
    model = RegistroRealizado

    def listar_por_historico(self, id_historico):
        return RegistroRealizado.query.filter_by(idHistorico=id_historico).all()

class FotoRegistroRepository(BaseRepository):
    model = FotoRegistro

    def listar_por_registro(self, id_registro):
        return FotoRegistro.query.filter_by(idRegistro=id_registro).all()
