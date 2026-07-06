import datetime

from models.notificacao_model import Notificacao
from repositories.notificacao_repository import NotificacaoRepository

class NotificacaoService:
    def __init__(self):
        self.repository = NotificacaoRepository()

    def listar_por_usuario(self, id_usuario, apenas_nao_lidas=False):
        return self.repository.listar_por_usuario(id_usuario, apenas_nao_lidas)

    def criar(self, dados):
        if not dados.get("idUsuario") or not dados.get("mensagem"):
            raise ValueError("idUsuario e mensagem são obrigatórios")

        notificacao = Notificacao(
            mensagem=dados["mensagem"],
            dataEnvio=datetime.datetime.utcnow(),
            lida=False,
            idUsuario=dados["idUsuario"],
            idEvento=dados.get("idEvento"),
        )
        self.repository.criar(notificacao)
        return notificacao

    def marcar_como_lida(self, id_notificacao, id_usuario):
        notificacao = self.repository.buscar_por_id(id_notificacao)
        if not notificacao or notificacao.idUsuario != id_usuario:
            raise ValueError("notificação não encontrada")
        notificacao.lida = True
        self.repository.atualizar()
        return notificacao
