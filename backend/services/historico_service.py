import datetime

from models.historico_model import HistoricoTrilha, RegistroRealizado, FotoRegistro
from repositories.historico_repository import (
    HistoricoRepository,
    RegistroRealizadoRepository,
    FotoRegistroRepository,
)

class HistoricoService:
    def __init__(self):
        self.repository = HistoricoRepository()
        self.registro_repository = RegistroRealizadoRepository()
        self.foto_repository = FotoRegistroRepository()

    def listar_por_usuario(self, id_usuario):
        return self.repository.listar_por_usuario(id_usuario)

    def buscar_por_id(self, id_historico):
        historico = self.repository.buscar_por_id(id_historico)
        if not historico:
            raise ValueError("histórico não encontrado")
        return historico

    def criar(self, id_usuario, dados):
        if not dados.get("idTrilha"):
            raise ValueError("idTrilha é obrigatório")

        historico = HistoricoTrilha(
            dataRealizacao=dados.get("dataRealizacao") or datetime.date.today(),
            tempo=dados.get("tempo"),
            avaliacaoPessoal=dados.get("avaliacaoPessoal"),
            idUsuario=id_usuario,
            idEvento=dados.get("idEvento"),
            idTrilha=dados["idTrilha"],
        )
        self.repository.criar(historico)
        return historico

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
        self.registro_repository.criar(registro)
        return registro

    def listar_registros(self, id_historico):
        return self.registro_repository.listar_por_historico(id_historico)

    def anexar_foto_registro(self, id_registro, dados):
        if not dados.get("url"):
            raise ValueError("url da foto é obrigatória")

        foto = FotoRegistro(
            url=dados["url"], legenda=dados.get("legenda"), idRegistro=id_registro
        )
        self.foto_repository.criar(foto)
        return foto

    def listar_fotos_registro(self, id_registro):
        return self.foto_repository.listar_por_registro(id_registro)
