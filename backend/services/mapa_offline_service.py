import datetime

from models.mapa_offline_model import MapaOffline
from repositories.mapa_offline_repository import MapaOfflineRepository

class MapaOfflineService:
    def __init__(self):
        self.repository = MapaOfflineRepository()

    def listar_por_trilha(self, id_trilha):
        return self.repository.listar_por_trilha(id_trilha)

    def registrar_download(self, dados):
        if not dados.get("idTrilha") or not dados.get("arquivoUrl"):
            raise ValueError("idTrilha e arquivoUrl são obrigatórios")

        mapa = MapaOffline(
            arquivoUrl=dados["arquivoUrl"],
            tamanhoArquivo=dados.get("tamanhoArquivo"),
            dataDownload=datetime.date.today(),
            idTrilha=dados["idTrilha"],
        )
        self.repository.criar(mapa)
        return mapa

    def deletar(self, id_mapa):
        mapa = self.repository.buscar_por_id(id_mapa)
        if not mapa:
            raise ValueError("mapa offline não encontrado")
        self.repository.deletar(mapa)
