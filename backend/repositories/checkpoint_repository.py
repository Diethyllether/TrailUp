from models.checkpoint_model import Checkpoint
from repositories.base_repository import BaseRepository

class CheckpointRepository(BaseRepository):
    model = Checkpoint

    def listar_por_trilha(self, id_trilha):
        return Checkpoint.query.filter_by(idTrilha=id_trilha).all()

    def primeiro_valido_por_trilha(self, id_trilha):
        checkpoints = Checkpoint.query.filter_by(idTrilha=id_trilha).order_by(
            Checkpoint.idCheckpoint.asc()
        )
        for checkpoint in checkpoints:
            latitude, longitude = checkpoint.latitude, checkpoint.longitude
            if (
                latitude is not None
                and longitude is not None
                and -90 <= latitude <= 90
                and -180 <= longitude <= 180
                and (latitude, longitude) != (0, 0)
            ):
                return checkpoint
        return None
