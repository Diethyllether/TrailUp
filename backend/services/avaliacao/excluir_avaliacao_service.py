from models.avaliacao_model import Avaliacao
from utils.excecoes import PermissaoNegada, RecursoNaoEncontrado


class ExcluirAvaliacaoService:
    def __init__(self, modelo_avaliacao=None):
        self.modelo_avaliacao = modelo_avaliacao or Avaliacao

    def executar(self, id_avaliacao, id_usuario):
        avaliacao = self.modelo_avaliacao.buscar_por_id(id_avaliacao)
        if avaliacao is None:
            raise RecursoNaoEncontrado("avaliação não encontrada")
        if avaliacao.idUsuario != id_usuario:
            raise PermissaoNegada("você só pode remover suas próprias avaliações")
        avaliacao.deletar()
        return {"excluida": True}
