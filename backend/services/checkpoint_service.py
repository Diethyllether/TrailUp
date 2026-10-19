import datetime

from models.checkpoint_model import Checkpoint

class CheckpointService:
    def __init__(self):
        pass

    def listar_por_trilha(self, id_trilha):
        return Checkpoint.listar_por_trilha(id_trilha)

    def buscar_por_id(self, id_checkpoint):
        checkpoint = Checkpoint.buscar_por_id(id_checkpoint)
        if not checkpoint:
            raise ValueError("checkpoint não encontrado")
        return checkpoint

    def criar(self, dados):
        if not dados.get("idTrilha"):
            raise ValueError("idTrilha é obrigatório")
        if dados.get("latitude") is None or dados.get("longitude") is None:
            raise ValueError("latitude e longitude são obrigatórias")

        checkpoint = Checkpoint(
            latitude=dados["latitude"],
            longitude=dados["longitude"],
            horario=dados.get("horario") or datetime.datetime.utcnow(),
            idTrilha=dados["idTrilha"],
        )
        return checkpoint.salvar()

    def deletar(self, id_checkpoint):
        checkpoint = self.buscar_por_id(id_checkpoint)
        checkpoint.deletar()
