from models.checkpoint_model import Checkpoint
from repositories.base_repository import BaseRepository

class CheckpointRepository(BaseRepository):
    model = Checkpoint

    def listar_por_trilha(self, id_trilha):
        return Checkpoint.query.filter_by(idTrilha=id_trilha).all()
