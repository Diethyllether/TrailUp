from models.favorito_model import Favorito
from repositories.trilha_repository import TrilhaRepository
from services.trilha.filtrar_trilhas_service import FiltrarTrilhasService
from services.trilha.listar_trilhas_proximas_service import ListarTrilhasProximasService
from utils.normalizacao import normalizar_dificuldade


class BuscarTrilhasService:
    def __init__(self, repository=None, service_filtros=None, service_proximas=None):
        self.repository = repository or TrilhaRepository()
        self.service_filtros = service_filtros or FiltrarTrilhasService(self.repository)
        self.service_proximas = service_proximas or ListarTrilhasProximasService(self.repository)

    def executar(
        self,
        termo=None,
        dificuldade=None,
        distancia_max=None,
        duracao_max=None,
        nota_min=None,
        ordem=None,
        latitude=None,
        longitude=None,
        id_usuario=None,
    ):
        encontradas = self.repository.buscar(
            busca=(termo or "").strip() or None,
            dificuldade=normalizar_dificuldade(dificuldade),
        )
        if any(valor not in (None, "") for valor in (distancia_max, duracao_max, nota_min, ordem)):
            filtradas = self.service_filtros.executar(
                distancia_max, duracao_max, nota_min, ordem
            )
            ids_filtrados = {item["idTrilha"] for item in filtradas}
            encontradas = [item for item in encontradas if item.idTrilha in ids_filtrados]
        distancias = {}
        if latitude not in (None, "") and longitude not in (None, ""):
            proximas = self.service_proximas.executar(latitude, longitude)
            distancias = {item["idTrilha"]: item["distanciaProxima"] for item in proximas}
            encontradas = [item for item in encontradas if item.idTrilha in distancias]
            encontradas.sort(key=lambda item: distancias[item.idTrilha])
        medias = self.repository.medias_avaliacao()
        favoritos = (
            {item.idTrilha for item in Favorito.listar_por_usuario(id_usuario)}
            if id_usuario
            else set()
        )
        return [
            {
                **trilha.to_dict(),
                "media": list(medias.get(trilha.idTrilha, (None, 0))),
                "favorito": trilha.idTrilha in favoritos,
                "distanciaProxima": distancias.get(trilha.idTrilha),
            }
            for trilha in encontradas
        ]
