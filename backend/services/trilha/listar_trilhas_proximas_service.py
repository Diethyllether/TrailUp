from models.trilha_model import Trilha
from repositories.trilha_repository import TrilhaRepository
from utils.excecoes import ErroDeValidacao


class ListarTrilhasProximasService:
    def __init__(self, repository=None, modelo_trilha=None):
        self.repository = repository or TrilhaRepository()
        self.modelo_trilha = modelo_trilha or Trilha

    def executar(self, latitude, longitude, limite=100):
        try:
            lat = float(latitude)
            lon = float(longitude)
            limite = int(limite)
        except (TypeError, ValueError) as error:
            raise ErroDeValidacao("coordenadas inválidas") from error
        if not -90 <= lat <= 90 or not -180 <= lon <= 180 or limite < 1:
            raise ErroDeValidacao("coordenadas ou limite fora do intervalo permitido")
        ids_e_distancias = self.repository.trilhas_proximas(lat, lon, limite)
        resultado = []
        for linha in ids_e_distancias:
            trilha = self.modelo_trilha.buscar_por_id(linha["idTrilha"])
            if trilha:
                resultado.append({**trilha.to_dict(), "distanciaProxima": round(float(linha["distanciaKm"]), 1)})
        return resultado
