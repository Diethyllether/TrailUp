from models.notificacao_model import Notificacao
from repositories.base_repository import BaseRepository

class NotificacaoRepository(BaseRepository):
    model = Notificacao

    def listar_por_usuario(self, id_usuario, apenas_nao_lidas=False):
        query = Notificacao.query.filter_by(idUsuario=id_usuario)
        if apenas_nao_lidas:
            query = query.filter_by(lida=False)
        return query.order_by(Notificacao.dataEnvio.desc()).all()
