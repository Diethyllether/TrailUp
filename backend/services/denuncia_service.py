import datetime

from models.denuncia_model import Denuncia


class DenunciaService:
    def __init__(self, repository=None):
        self.repository = repository

    def listar_por_evento(self, id_evento):
        return Denuncia.listar_por_evento(id_evento)

    def criar(self, id_usuario_denunciante, dados):
        descricao = (dados.get("descricao") or "").strip()
        categoria = dados.get("categoria", "EVENTO")
        if not descricao or categoria not in ("BUG", "TRILHA", "EVENTO", "OUTRO"):
            raise ValueError("categoria e descrição válida são obrigatórias")
        if categoria == "EVENTO" and not dados.get("idEvento"):
            raise ValueError("evento não encontrado")
        if categoria == "TRILHA" and not dados.get("idTrilha"):
            raise ValueError("trilha não encontrada")
        denuncia = Denuncia(
            descricao=descricao,
            dataEnvio=datetime.datetime.utcnow(),
            status="PENDENTE",
            categoria=categoria,
            idEvento=dados.get("idEvento"),
            idTrilha=dados.get("idTrilha"),
            idUsuarioDenunciante=id_usuario_denunciante,
            idUsuarioDenunciado=dados.get("idUsuarioDenunciado"),
        )
        return denuncia.salvar()

    def atualizar_status(self, id_denuncia, status):
        denuncia = Denuncia.buscar_por_id(id_denuncia)
        if not denuncia:
            raise ValueError("denúncia não encontrada")
        if status not in ("PENDENTE", "EM_ANALISE", "RESOLVIDA", "ARQUIVADA"):
            raise ValueError("status inválido")
        denuncia.status = status
        return denuncia.atualizar()
