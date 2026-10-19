from datetime import date

from models.historico_model import HistoricoTrilha
from models.trilha_model import Trilha
from utils.excecoes import ErroDeValidacao, RecursoNaoEncontrado


class RegistrarTrilhaConcluidaService:
    def __init__(self, modelo_historico=None, modelo_trilha=None):
        self.modelo_historico = modelo_historico or HistoricoTrilha
        self.modelo_trilha = modelo_trilha or Trilha

    def executar(self, id_usuario, dados):
        try:
            id_trilha = int(dados.get("idTrilha"))
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("idTrilha é obrigatório") from error
        if not self.modelo_trilha.buscar_por_id(id_trilha):
            raise RecursoNaoEncontrado("trilha não encontrada")
        tempo = dados.get("tempo")
        avaliacao = dados.get("avaliacaoPessoal")
        try:
            tempo = float(tempo) if tempo not in (None, "") else None
            avaliacao = int(avaliacao) if avaliacao not in (None, "") else None
            dia = date.fromisoformat(dados["dataRealizacao"]) if dados.get("dataRealizacao") else date.today()
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("data, tempo ou avaliação inválidos") from error
        if tempo is not None and tempo < 0:
            raise ErroDeValidacao("tempo deve ser zero ou maior")
        if avaliacao is not None and avaliacao not in range(1, 6):
            raise ErroDeValidacao("avaliação deve ser de 1 a 5")
        historico = self.modelo_historico(
            dataRealizacao=dia, tempo=tempo, avaliacaoPessoal=avaliacao,
            idUsuario=id_usuario, idEvento=dados.get("idEvento"), idTrilha=id_trilha,
        ).salvar()
        return historico.to_dict()
