from datetime import datetime

from models.denuncia_model import Denuncia
from models.evento_model import Evento
from models.trilha_model import Trilha
from utils.excecoes import ErroDeValidacao, RecursoNaoEncontrado


class ReportarProblemaService:
    def __init__(self, modelo_denuncia=None, modelo_evento=None, modelo_trilha=None):
        self.modelo_denuncia = modelo_denuncia or Denuncia
        self.modelo_evento = modelo_evento or Evento
        self.modelo_trilha = modelo_trilha or Trilha

    def executar(self, id_usuario, dados):
        descricao = (dados.get("descricao") or "").strip()
        categoria = dados.get("categoria", "EVENTO")
        if not descricao or categoria not in ("BUG", "TRILHA", "EVENTO", "OUTRO"):
            raise ErroDeValidacao("categoria e descrição válida são obrigatórias")
        id_evento = dados.get("idEvento")
        id_trilha = dados.get("idTrilha")
        if categoria == "EVENTO" and (
            not id_evento or not self.modelo_evento.buscar_por_id(id_evento)
        ):
            raise RecursoNaoEncontrado("evento não encontrado")
        if categoria == "TRILHA" and (
            not id_trilha or not self.modelo_trilha.buscar_por_id(id_trilha)
        ):
            raise RecursoNaoEncontrado("trilha não encontrada")
        denuncia = self.modelo_denuncia(
            descricao=descricao,
            dataEnvio=datetime.utcnow(),
            status="PENDENTE",
            categoria=categoria,
            idEvento=id_evento,
            idTrilha=id_trilha,
            idUsuarioDenunciante=id_usuario,
            idUsuarioDenunciado=dados.get("idUsuarioDenunciado"),
        ).salvar()
        return denuncia.to_dict()
