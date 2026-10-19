import datetime

from models.avaliacao_model import Avaliacao


class AvaliacaoService:
    def __init__(self, repository=None):
        self.repository = repository

    def listar_por_trilha(self, id_trilha):
        return Avaliacao.query.filter_by(idTrilha=id_trilha).all()

    def listar_por_usuario(self, id_usuario):
        return Avaliacao.query.filter_by(idUsuario=id_usuario).all()

    def media_por_trilha(self, id_trilha):
        avaliacoes = self.listar_por_trilha(id_trilha)
        return round(sum(a.nota for a in avaliacoes) / len(avaliacoes), 1) if avaliacoes else None

    def buscar_por_id(self, id_avaliacao):
        avaliacao = Avaliacao.buscar_por_id(id_avaliacao)
        if not avaliacao:
            raise ValueError("avaliação não encontrada")
        return avaliacao

    @staticmethod
    def _nota_valida(valor):
        try:
            nota = int(valor)
        except (TypeError, ValueError):
            raise ValueError("nota deve ser um número entre 1 e 5")
        if str(valor).strip() not in (str(nota), f"{nota}.0") or not 1 <= nota <= 5:
            raise ValueError("nota deve ser um número entre 1 e 5")
        return nota

    def criar(self, id_usuario, dados):
        nota = self._nota_valida(dados.get("nota"))
        if not dados.get("idTrilha"):
            raise ValueError("idTrilha é obrigatório")
        avaliacao = Avaliacao(nota=nota, comentario=dados.get("comentario"),
                              data=datetime.date.today(), idUsuario=id_usuario,
                              idTrilha=dados["idTrilha"])
        return avaliacao.salvar()

    def atualizar(self, id_avaliacao, id_usuario, dados):
        avaliacao = self.buscar_por_id(id_avaliacao)
        if avaliacao.idUsuario != id_usuario:
            raise PermissionError("você só pode editar suas próprias avaliações")
        if "nota" in dados:
            avaliacao.nota = self._nota_valida(dados["nota"])
        if "comentario" in dados:
            avaliacao.comentario = dados["comentario"]
        return avaliacao.atualizar()

    def deletar(self, id_avaliacao, id_usuario):
        avaliacao = self.buscar_por_id(id_avaliacao)
        if avaliacao.idUsuario != id_usuario:
            raise PermissionError("você só pode remover suas próprias avaliações")
        avaliacao.deletar()
