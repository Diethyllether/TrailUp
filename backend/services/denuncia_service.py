import datetime

from models.denuncia_model import Denuncia
from repositories.denuncia_repository import DenunciaRepository

class DenunciaService:
    def __init__(self):
        self.repository = DenunciaRepository()

    def listar_por_evento(self, id_evento):
        return self.repository.listar_por_evento(id_evento)

    def criar(self, id_usuario_denunciante, dados):
        if not dados.get("idEvento") or not dados.get("descricao"):
            raise ValueError("idEvento e descricao são obrigatórios")

        denuncia = Denuncia(
            descricao=dados["descricao"],
            dataEnvio=datetime.datetime.utcnow(),
            status="PENDENTE",
            idEvento=dados["idEvento"],
            idUsuarioDenunciante=id_usuario_denunciante,
            idUsuarioDenunciado=dados.get("idUsuarioDenunciado"),
        )
        self.repository.criar(denuncia)
        return denuncia

    def atualizar_status(self, id_denuncia, status):
        denuncia = self.repository.buscar_por_id(id_denuncia)
        if not denuncia:
            raise ValueError("denúncia não encontrada")
        if status not in ("PENDENTE", "EM_ANALISE", "RESOLVIDA", "ARQUIVADA"):
            raise ValueError("status inválido")
        denuncia.status = status
        self.repository.atualizar()
        return denuncia
