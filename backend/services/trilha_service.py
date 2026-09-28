import unicodedata
import math

from models.trilha_model import Trilha
from repositories.trilha_repository import TrilhaRepository
from services.casos_uso import BuscarTrilhasService, DetalharTrilhaService

VELOCIDADE_POR_DIFICULDADE = {
    "FACIL": 4.0,
    "MODERADA": 3.0,
    "DIFICIL": 2.0,
}

def _normalizar_dificuldade(valor):
    if not valor:
        return valor
    sem_acento = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode()
    codigo = sem_acento.strip().upper()
    if codigo in ("MODERADO", "MODERADA"):
        return "MODERADA"
    if codigo in VELOCIDADE_POR_DIFICULDADE:
        return codigo
    return valor

class TrilhaService:
    """Facade de trilha; busca e detalhe possuem Services de caso de uso."""

    def __init__(self, repository=None):
        self.repository = repository or TrilhaRepository()
        self.buscar_service = BuscarTrilhasService(self.repository)
        self.detalhar_service = DetalharTrilhaService(self.repository)

    @staticmethod
    def calcular_tempo_estimado_min(distancia_km, dificuldade):
        if not distancia_km:
            return None
        velocidade = VELOCIDADE_POR_DIFICULDADE.get((dificuldade or "").upper(), 3.0)
        horas = distancia_km / velocidade
        return round(horas * 60, 1)

    def listar_todos(self):
        return self.repository.listar_todos()

    def listar_ordenadas(self, ordenacao=None, distancia_max=None, duracao_max=None, nota_min=None):
        return self.repository.listar_ordenadas(ordenacao, distancia_max, duracao_max, nota_min)

    def medias_avaliacao(self):
        return self.repository.medias_avaliacao()

    def proximas(self, latitude, longitude, limite=6):
        pontos = {}
        for cp in self.repository.pontos_proximos():
            pontos.setdefault(cp.idTrilha, (cp.latitude, cp.longitude))
        trilhas = {t.idTrilha: t for t in self.listar_todos()}
        def distancia(coord):
            lat, lon = coord
            a, b = math.radians(latitude), math.radians(lat)
            dlat, dlon = b-a, math.radians(lon-longitude)
            h = math.sin(dlat/2)**2 + math.cos(a)*math.cos(b)*math.sin(dlon/2)**2
            return 6371 * 2 * math.asin(math.sqrt(h))
        resultados = [(trilhas[i], round(distancia(p), 1)) for i,p in pontos.items() if i in trilhas]
        return sorted(resultados, key=lambda item: item[1])[:limite]
        

    def buscar(self, nome=None, localizacao=None, dificuldade=None, busca=None):
        return self.buscar_service.executar(
            nome=nome,
            localizacao=localizacao,
            dificuldade=dificuldade,
            busca=busca,
        )

    def buscar_por_id(self, id_trilha):
        return self.detalhar_service.executar(id_trilha)

    def criar(self, dados):
        if not dados.get("nome"):
            raise ValueError("nome da trilha é obrigatório")

        tempo_estimado = self.calcular_tempo_estimado_min(
            dados.get("distancia"), dados.get("dificuldade")
        )
        trilha = Trilha(
            nome=dados["nome"],
            localizacao=dados.get("localizacao"),
            distancia=dados.get("distancia"),
            duracao=dados.get("duracao"),
            dificuldade=_normalizar_dificuldade(dados.get("dificuldade")),
            descricao=dados.get("descricao"),
            imagemUrl=dados.get("imagemUrl"),
            tempoEstimadoMin=tempo_estimado,
        )
        return self.repository.criar(trilha)

    def atualizar(self, id_trilha, dados):
        trilha = self.buscar_por_id(id_trilha)

        for campo in ("nome", "localizacao", "distancia", "duracao", "dificuldade", "descricao", "imagemUrl"):
            if campo in dados:
                valor = dados[campo]
                if campo == "dificuldade":
                    valor = _normalizar_dificuldade(valor)
                setattr(trilha, campo, valor)

        trilha.tempoEstimadoMin = self.calcular_tempo_estimado_min(
            trilha.distancia, trilha.dificuldade
        )
        self.repository.atualizar()
        return trilha

    def deletar(self, id_trilha):
        trilha = self.buscar_por_id(id_trilha)
        self.repository.deletar(trilha)
