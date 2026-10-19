import datetime

from models.historico_model import HistoricoTrilha
from models.registro_realizado_model import RegistroRealizado

class HistoricoService:
    def __init__(self):
        pass

    def listar_por_usuario(self, id_usuario):
        return HistoricoTrilha.query.filter_by(idUsuario=id_usuario).all()

    def buscar_por_id(self, id_historico):
        historico = HistoricoTrilha.buscar_por_id(id_historico)
        if not historico:
            raise ValueError("histórico não encontrado")
        return historico

    def criar(self, id_usuario, dados):
        if not dados.get("idTrilha"):
            raise ValueError("idTrilha é obrigatório")

        tempo = dados.get("tempo")
        if tempo not in (None, "") and float(tempo) < 0:
            raise ValueError("tempo deve ser zero ou maior")
        avaliacao = dados.get("avaliacaoPessoal")
        if avaliacao not in (None, "") and int(avaliacao) not in range(1, 6):
            raise ValueError("avaliação pessoal deve ser de 1 a 5")

        historico = HistoricoTrilha(
            dataRealizacao=dados.get("dataRealizacao") or datetime.date.today(),
            tempo=float(tempo) if tempo not in (None, "") else None,
            avaliacaoPessoal=int(avaliacao) if avaliacao not in (None, "") else None,
            idUsuario=id_usuario,
            idEvento=dados.get("idEvento"),
            idTrilha=dados["idTrilha"],
        )
        return historico.salvar()

    def registrar_checkpoint(self, id_historico, dados):
        if dados.get("latitude") is None or dados.get("longitude") is None:
            raise ValueError("latitude e longitude são obrigatórias")

        registro = RegistroRealizado(
            latitude=dados["latitude"],
            longitude=dados["longitude"],
            horario=dados.get("horario") or datetime.datetime.utcnow(),
            observacao=dados.get("observacao"),
            idHistorico=id_historico,
        )
        return registro.salvar()

    def listar_registros(self, id_historico):
        return RegistroRealizado.query.filter_by(idHistorico=id_historico).all()
