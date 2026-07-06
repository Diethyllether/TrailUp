import datetime

from models.avaliacao_model import Avaliacao
from repositories.avaliacao_repository import AvaliacaoRepository

class AvaliacaoService:
    def __init__(self):
        self.repository = AvaliacaoRepository()

    def listar_por_trilha(self, id_trilha):
        return self.repository.listar_por_trilha(id_trilha)

    def buscar_por_id(self, id_avaliacao):
        avaliacao = self.repository.buscar_por_id(id_avaliacao)
        if not avaliacao:
            raise ValueError("avaliação não encontrada")
        return avaliacao

    def criar(self, id_usuario, dados):
        nota = dados.get("nota")
        if nota is None or not (1 <= int(nota) <= 5):
            raise ValueError("nota deve ser um número entre 1 e 5")
        if not dados.get("idTrilha"):
            raise ValueError("idTrilha é obrigatório")

        avaliacao = Avaliacao(
            nota=nota,
            comentario=dados.get("comentario"),
            data=datetime.date.today(),
            idUsuario=id_usuario,
            idTrilha=dados["idTrilha"],
        )
        self.repository.criar(avaliacao)
        return avaliacao

    def atualizar(self, id_avaliacao, id_usuario, dados):
        avaliacao = self.buscar_por_id(id_avaliacao)
        if avaliacao.idUsuario != id_usuario:
            raise PermissionError("você só pode editar suas próprias avaliações")

        if "nota" in dados:
            avaliacao.nota = dados["nota"]
        if "comentario" in dados:
            avaliacao.comentario = dados["comentario"]

        self.repository.atualizar()
        return avaliacao

    def deletar(self, id_avaliacao, id_usuario):
        avaliacao = self.buscar_por_id(id_avaliacao)
        if avaliacao.idUsuario != id_usuario:
            raise PermissionError("você só pode remover suas próprias avaliações")
        self.repository.deletar(avaliacao)
