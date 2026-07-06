from models.mapa_offline_model import MapaOffline
from repositories.base_repository import BaseRepository

class MapaOfflineRepository(BaseRepository):
    model = MapaOffline

    def listar_por_trilha(self, id_trilha):
        return MapaOffline.query.filter_by(idTrilha=id_trilha).all()
