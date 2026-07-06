from models.foto_model import Foto
from repositories.base_repository import BaseRepository

class FotoRepository(BaseRepository):
    model = Foto

    def listar_por_trilha(self, id_trilha):
        return Foto.query.filter_by(idTrilha=id_trilha).all()
