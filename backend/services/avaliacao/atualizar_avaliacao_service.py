from models.avaliacao_model import Avaliacao
from utils.excecoes import ErroDeValidacao, PermissaoNegada, RecursoNaoEncontrado


class AtualizarAvaliacaoService:
    def __init__(self, modelo_avaliacao=None):
        self.modelo_avaliacao = modelo_avaliacao or Avaliacao

    def executar(self, id_avaliacao, id_usuario, dados):
        avaliacao = self.modelo_avaliacao.buscar_por_id(id_avaliacao)
        if avaliacao is None:
            raise RecursoNaoEncontrado("avaliação não encontrada")
        if avaliacao.idUsuario != id_usuario:
            raise PermissaoNegada("você só pode editar suas próprias avaliações")
        if "nota" in dados:
            try:
                nota = int(dados["nota"])
            except (TypeError, ValueError) as error:
                raise ErroDeValidacao("nota deve ser um número entre 1 e 5") from error
            if str(dados["nota"]).strip() not in (str(nota), f"{nota}.0") or nota not in range(1, 6):
                raise ErroDeValidacao("nota deve ser um número entre 1 e 5")
            avaliacao.nota = nota
        if "comentario" in dados:
            avaliacao.comentario = dados["comentario"]
        return avaliacao.atualizar().to_dict()
