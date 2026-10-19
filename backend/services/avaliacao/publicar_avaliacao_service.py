from datetime import date

from models.avaliacao_model import Avaliacao
from models.trilha_model import Trilha
from utils.excecoes import ErroDeValidacao, RecursoNaoEncontrado


class PublicarAvaliacaoService:
    def __init__(self, modelo_avaliacao=None, modelo_trilha=None):
        self.modelo_avaliacao = modelo_avaliacao or Avaliacao
        self.modelo_trilha = modelo_trilha or Trilha

    def executar(self, id_usuario, id_trilha, dados):
        if not self.modelo_trilha.buscar_por_id(id_trilha):
            raise RecursoNaoEncontrado("trilha não encontrada")
        try:
            nota = int(dados.get("nota"))
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("nota deve ser um número entre 1 e 5") from error
        if str(dados.get("nota")).strip() not in (str(nota), f"{nota}.0") or nota not in range(1, 6):
            raise ErroDeValidacao("nota deve ser um número entre 1 e 5")
        avaliacao = self.modelo_avaliacao(
            nota=nota, comentario=dados.get("comentario"), data=date.today(),
            idUsuario=id_usuario, idTrilha=id_trilha,
        ).salvar()
        return avaliacao.to_dict()
